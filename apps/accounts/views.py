from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'accounts/signup.html')

from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/jobs')
        else:
            from django.contrib import messages
            messages.error(request, "Invalid credentials")

    return render(request, 'accounts/login.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')