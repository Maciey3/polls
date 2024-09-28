from django.shortcuts import render, redirect
from .models import Poll, Option
from .forms import PollForm


def home(request):
    polls = Poll.objects.all()
    context = {'polls': polls}
    return render(request, 'base/home.html', context)

def poll(request, pk):
    poll = Poll.objects.get(id=pk)
    options = Option.objects.filter(poll_id=pk)
    context = {
        'poll': poll,
        'options': options,
    }
    return render(request, 'base/poll.html', context)

def create_poll(request):
    form = PollForm()
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/poll_form.html', context)

def update_poll(request, pk):
    poll = Poll.objects.get(id=pk)
    form = PollForm(instance=poll)

    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        if form .is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/poll_form.html', context)

def delete_poll(request, pk):
    poll = Poll.objects.get(id=pk)
    if request.method == 'POST':
        poll.delete()
        return redirect('home')

    context = {'obj': poll}
    return render(request, 'base/delete.html', context)