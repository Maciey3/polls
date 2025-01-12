from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST
from .models import Poll, Option, Vote, Style, Tag
from comments.models import Comment
import json
from datetime import datetime, timedelta, timezone


def home(request):
    def cut_poll_description(poll):
        poll.question = f"{poll.question[:question_len]}..."
        return poll

    question_len = 250
    q = request.GET.get('q') if request.GET.get('q') else ''
    q_tags = request.GET.getlist('tags') if request.GET.get('tags') else ''
    q_tags = [int(item) for item in q_tags]

    polls = Poll.objects.filter(
        Q(question__icontains=q) | Q(description__icontains=q),
        Q(tags__id__in=q_tags)
        if q_tags else Q(question__icontains=q) | Q(description__icontains=q)
    ).distinct()

    tags = Tag.objects.all()

    polls_shortened = [poll if len(poll.question) < question_len else cut_poll_description(poll) for poll in polls]
    context = {
        'polls': polls_shortened,
        'search': q,
        'search_tags': q_tags,
        'tags': tags
    }

    return render(request, 'base/home.html', context)

def poll(request, pk):
    def compute_percent(votes, options):
        tmp = {}

        for vote in votes:
            option = vote.option
            if option.label not in tmp:
                tmp[option.label] = 1
            else:
                tmp[option.label] += 1

        for option in options:
            if option.label in tmp:
                option.percent = tmp[option.label] / len(votes) * 100
            else:
                option.percent = 0
        # print(tmp.keys(), tmp.values())
        return options, tmp

    poll = Poll.objects.get(id=pk)
    options = poll.options
    votes = Vote.objects.filter(poll_id=pk)

    comments = poll.comments.annotate(
        votes_sum=Count('commentvote', filter=Q(commentvote__vote=True)) -
                  Count('commentvote', filter=Q(commentvote__vote=False))
    ).order_by('-votes_sum')
    # Comment.objects

    for comment in comments:
        timediff = datetime.now(timezone.utc) - comment.created
        if timediff.days >= 1:
            comment.time_ago = f'{timediff.days} days ago'
        elif timediff.seconds // 3600 > 1:
            comment.time_ago = f'{timediff.seconds // 3600} hours ago'
        else:
            comment.time_ago = f'{timediff.seconds // 60} minutes ago'

        if request.user.is_authenticated:
            if any(vote.user == request.user and vote.vote == 1 for vote in comment.votes):
                comment.has_voted_positive = True
            elif any(vote.user == request.user and vote.vote == 0 for vote in comment.votes):
                comment.has_voted_negative = True


    options, js_dict = compute_percent(votes, options)

    user_vote = votes.filter(user_id=request.user.id)

    context = {
        'poll': poll,
        'options': options,
        'already_voted': user_vote.exists(),
        'vote_id': user_vote.get().option_id if user_vote else None,
        'js_keys': json.dumps(list(js_dict.keys())),
        'js_values': json.dumps(list(js_dict.values())),
        'comments': comments
    }
    return render(request, 'base/poll.html', context)

@login_required(login_url='login')
def create_poll(request):
    styles = Style.objects.all()
    tags = Tag.objects.all()
    context = {
        'action': 'store-poll',
        'styles': styles,
        'tags': tags
    }
    return render(request, 'base/poll_form.html', context)

@login_required(login_url='login')
@require_POST
def store_poll(request):
    print(request.POST)
    question = request.POST.get('question')
    description = request.POST.get('description')
    options = request.POST.getlist('options[]')
    style = request.POST.getlist('styles[]')
    tags = request.POST.getlist('tags')

    if not style:
        messages.error(request, "Style is required")
        return redirect('create-poll')

    poll = Poll.objects.create(
        question=question,
        description=description,
        made_by=request.user,
    )

    poll.styles.add(Style.objects.get(id=style[0]))

    for option in options:
        Option.objects.create(
            label=option,
            poll=poll
        )

    poll.tags.add(*tags)

    messages.success(request, "Poll created successfully!")
    return redirect('home')

@login_required(login_url='login')
def edit_poll(request, pk):
    poll = Poll.objects.get(id=pk)
    options = Option.objects.filter(poll=poll)
    styles = Style.objects.all()
    tags = Tag.objects.all()

    if request.user != poll.made_by:
        messages.error(request, "You are not allowed to edit this poll.")
        return redirect('home')

    context = {
        'action': "update-poll",
        'styles': styles,
        'action_id': pk,
        'poll': poll,
        'options': options,
        'tags': tags
    }
    return render(request, 'base/poll_form.html', context)

def update_poll(request, pk):
    question = request.POST.get('question')
    description = request.POST.get('description')
    options = request.POST.getlist('options[]')
    styles = request.POST.getlist('styles[]')
    tags = request.POST.getlist('tags')

    if not styles:
        messages.error(request, "Style is required")
        return redirect('edit-poll', pk)


    Poll.objects.filter(id=pk).update(
        question=question,
        description=description
    )

    poll = Poll.objects.get(id=pk)
    previous_options = poll.options
    [option.delete() for option in previous_options]

    for option in options:
        Option.objects.create(
            label=option.strip(),
            poll=poll
        )

    poll.styles.clear()
    poll.styles.add(styles[0])

    poll.tags.clear()
    poll.tags.add(*tags)

    messages.success(request, "Poll edited successfully!")
    return redirect('home')

@login_required(login_url='login')
def delete_poll(request, pk):
    poll = Poll.objects.get(id=pk)

    if request.user != poll.made_by:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        poll.delete()
        messages.success(request, "Poll deleted successfully!")
        return redirect('home')

    context = {'obj': poll}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def vote(request, pk):
    option_id = request.POST.get('vote')
    user_id = request.user.id
    poll_id = pk
    if request.method == 'POST':
        Vote.objects.create(
            option_id=option_id,
            poll_id=poll_id,
            user_id=user_id
        )
    messages.success(request, "Voted successfully!")
    return redirect('poll', pk)

def delete_vote(request, pk):
    Vote.objects.filter(
        Q(poll_id=pk) & Q(user_id=request.user.id)
    ).delete()

    messages.success(request, "Vote deleted successfully!")
    return redirect('poll', pk)

def seed(request):
    Style.objects.create(
        name='Purple to pink gradient',
        tailwind_classes='bg-gradient-to-br from-purple-500 to-pink-500'
    )
    Style.objects.create(
        name='Green to blue gradient',
        tailwind_classes='bg-gradient-to-br from-green-500 to-blue-500'
    )
    Style.objects.create(
        name='Red to pink gradient',
        tailwind_classes='bg-gradient-to-br from-red-300 to-pink-500'
    )
    Style.objects.create(
        name='Orange border',
        tailwind_classes='bg-orange-300 border-4 border-orange-500'
    )
    Style.objects.create(
        name='White dashed border with dark blue background',
        tailwind_classes='border-4 bg-indigo-800 border-white border-dashed'
    )

    Tag.objects.create(
        name='Funny'
    )
    Tag.objects.create(
        name='Adult'
    )
    Tag.objects.create(
        name='Cars'
    )
    Tag.objects.create(
        name='Business'
    )
    Tag.objects.create(
        name='School'
    )

    return redirect('home')