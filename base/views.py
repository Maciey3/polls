from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST
from .models import Poll, Option, Vote, Style
import json


def home(request):
    def cut_poll_description(poll):
        poll.question = f"{poll.question[:question_len]}..."
        return poll

    question_len = 250
    q = request.GET.get('q') if request.GET.get('q') else ''
    polls = Poll.objects.filter(
        Q(question__icontains=q) | Q(description__icontains=q)
    )
    print(polls.first().styles.get().id)
    polls_shortened = [poll if len(poll.question) < question_len else cut_poll_description(poll) for poll in polls]
    context = {'polls': polls_shortened, 'search': q}
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
    options = poll.option_set.all()
    votes = Vote.objects.filter(poll_id=pk)
    options, js_dict = compute_percent(votes, options)

    user_vote = votes.filter(user_id=request.user.id)

    print(list(js_dict.keys()))

    context = {
        'poll': poll,
        'options': options,
        'already_voted': user_vote.exists(),
        'vote_id': user_vote.get().option_id if user_vote else None,
        'js_keys': json.dumps(list(js_dict.keys())),
        'js_values': json.dumps(list(js_dict.values())),
    }
    return render(request, 'base/poll.html', context)

@login_required(login_url='login')
def create_poll(request):
    styles = Style.objects.all()
    context = {'action': 'store-poll', 'styles': styles}
    return render(request, 'base/poll_form.html', context)

@login_required(login_url='login')
@require_POST
def store_poll(request):
    print(request.POST)
    question = request.POST.get('question')
    description = request.POST.get('description')
    options = request.POST.getlist('options[]')
    style = request.POST.get('style')


    poll = Poll.objects.create(
        question=question,
        description=description,
        made_by=request.user,
    )

    poll.styles.add(Style.objects.get(id=style))

    for option in options:
        Option.objects.create(
            label=option,
            poll=poll
        )

    messages.success(request, "Poll created successfully!")
    return redirect('home')

@login_required(login_url='login')
def edit_poll(request, pk):
    poll = Poll.objects.get(id=pk)
    options = Option.objects.filter(poll=poll)

    if request.user != poll.made_by:
        messages.error(request, "You are not allowed to edit this poll.")
        return redirect('home')


    context = {
        'action': "update-poll",
        'action_id': pk,
        'poll' : poll,
        'options': options
    }
    return render(request, 'base/poll_form.html', context)

def update_poll(request, pk):
    question = request.POST.get('question')
    description = request.POST.get('description')
    options = request.POST.getlist('options[]')

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