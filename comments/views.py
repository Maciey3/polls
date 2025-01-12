from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.contrib import messages
from django.urls import reverse
from comments.models import Comment, CommentVote
from base.models import Poll
from django.db.models import Count, Q, IntegerField, ExpressionWrapper, F
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
# Create your views here.

@login_required(login_url='login')
def create(request, poll_id):
    text = request.POST.get('comment')
    poll = Poll.objects.get(pk=poll_id)
    Comment.objects.create(
        user=request.user,
        poll=poll,
        text=text,
    )
    messages.success(request, "Comment was created")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def get_comments(poll):
    return Comment.objects.filter(poll=poll)

def htmx_vote(request, comment_id, vote):
    if not request.user.is_authenticated:
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = reverse('login')
            return response
        else:
            return redirect('login')

    comment = Comment.objects.get(id=comment_id)
    vote_comment(request.user, comment, vote)

    return HttpResponse(votes_html(request, comment.poll))
    # return HttpResponse('Ok')

def vote_comment(user, comment, vote):
    CommentVote.objects.update_or_create(
        user=user,
        comment=comment,
        defaults={'vote': vote}
    )


def votes_html(request, poll_id):
    result = ''
    # comments = Comment.objects.filter(poll=poll_id)
    comments = Comment.objects.annotate(
        votes_sum=Count('commentvote', filter=Q(commentvote__vote=True)) -
                  Count('commentvote', filter=Q(commentvote__vote=False))
        ).filter(poll=poll_id).order_by('-votes_sum')

    for comment in comments:
        timediff = datetime.now(timezone.utc) - comment.created
        if timediff.days >= 1:
            comment.time_ago = f'{timediff.days} days ago'
        elif timediff.seconds // 3600 > 1:
            comment.time_ago = f'{timediff.seconds // 3600} hours ago'
        else:
            comment.time_ago = f'{timediff.seconds // 60} minutes ago'

        flag = None
        if any(vote.user == request.user and vote.vote == 1 for vote in comment.votes):
            flag = True
        elif any(vote.user == request.user and vote.vote == 0 for vote in comment.votes):
            flag = False

        result += '<div class="flex gap-x-6 mt-6">'
        if comment.user.profile.image:
            result += f'<img class="rounded-full w-8 h-8" src="{comment.user.profile.image.url}" />'
        else:
            result += '<i class="text-2xl self-center fa-regular fa-circle-user"></i>'
        result += '<div class="w-full grid grid-cols-1">'
        result += '<div class="flex justify-between text-sm">'
        result += f'<p class="font-bold">@{comment.user.username}</p>'
        result += f'<p>{comment.time_ago}</p>'
        result += '</div>'
        result += f'<p>{comment.text}</p>'
        result += '<div class="flex items-center gap-x-2">'
        result += f'<p>{comment.sum_of_votes}</p>'
        result += f'<i hx-get="{reverse('vote-comment', args=[comment.id, 1])}" hx-target="#comment-container" class="text-xs fa-solid fa-thumbs-up cursor-pointer hover:text-blue-500 {'text-blue-500' if flag == 1 else ''}"></i>'
        result += f'<i hx-get="{reverse('vote-comment', args=[comment.id, 0])}" hx-target="#comment-container" class="text-xs fa-solid fa-thumbs-down cursor-pointer hover:text-blue-500 {'text-blue-500' if flag == 0 else ''}"></i>'
        result += '</div></div></div>'

    return result
