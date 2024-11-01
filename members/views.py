from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from members.models import Profile


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.filter(username=username, password=password).get()
        except:
            messages.error(request, "User doesn't exist or password is incorrect")
            context = {'page': page}
            return render(request, 'members/login.html', context)

        # user = authenticate(username=username, password=password)
        # print(user)
        if True is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesnt exist")

    context = {'page': page}
    return render(request, 'members/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    context = {}
    return render(request, 'members/register.html', context)

@require_POST
def register(request):
    username = request.POST.get('username').lower()
    password = request.POST.get('password')
    repassword = request.POST.get('re-password')

    if password != repassword:
        messages.error(request, 'Passwords dont match.')
        return redirect('register-page')

    user = User.objects.create(
        username=username,
        password=password
    )

    login(request, user)
    messages.success(request, 'Successfully registered!')
    return redirect('home')

def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'members/profile.html', context)

@require_POST
def profile_update(request):
    username = request.POST.get('username')
    bio = request.POST.get('bio')
    if request.FILES:
        image = request.FILES['image']
    else:
        image = None

    user = request.user

    if image:
        fs = FileSystemStorage(location='media/profiles')
        filename = fs.save(image.name, image)
        user.profile.image = f"profiles/{filename}"

    user.username = username
    user.profile.bio = bio
    user.save()

    messages.success(request, 'Succesfully updated the profile')
    return redirect('members.profile')

