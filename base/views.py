from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_http_methods, require_POST
from .models import Poll, Option, Vote
from .forms import PollForm

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesnt exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesnt exist")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_page(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

def home(request):
    def cut_poll_description(poll):
        poll.question = f"{poll.question[:question_len]}..."
        return poll

    question_len = 250
    q = request.GET.get('q') if request.GET.get('q') else ''
    polls = Poll.objects.filter(
        Q(question__icontains=q) | Q(description__icontains=q)
    )
    polls_shortened = [poll if len(poll.question) < question_len else cut_poll_description(poll) for poll in polls]
    context = {'polls': polls_shortened, 'search': q}
    return render(request, 'base/home.html', context)

def poll(request, pk):
    poll = Poll.objects.get(id=pk)
    options = poll.option_set.all()
    already_voted = Vote.objects.filter(
        Q(poll_id=pk) & Q(user_id=request.user.id)
    ).exists()
    context = {
        'poll': poll,
        'options': options,
        'already_voted': already_voted
    }
    return render(request, 'base/poll.html', context)

@login_required(login_url='login')

def create_poll(request):
    context = {'action': 'store-poll'}
    return render(request, 'base/poll_form.html', context)

@login_required(login_url='login')
@require_POST
def store_poll(request):
    print(request.POST)
    question = request.POST.get('question')
    description = request.POST.get('description')
    options = request.POST.getlist('options[]')

    poll = Poll.objects.create(
        question=question,
        description=description,
        made_by=request.user
    )

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

    poll = Poll.objects.filter(id=pk).update(
        question=question,
        description=description
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