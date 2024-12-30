from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from comments.models import Comment
from base.models import Poll

# Create your views here.

def create(request, poll_id):
    text = request.POST.get('comment')
    print(text)
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
