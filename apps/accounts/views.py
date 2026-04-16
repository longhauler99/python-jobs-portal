from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Validation
        if not all([first_name, last_name, email, password]):
            messages.error(request, "All fields are required")
            return redirect("signup")

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        user.first_name = first_name,
        user.last_name = last_name,
        user.save()


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