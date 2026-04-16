from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

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

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('jobs')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('login')

    return redirect('home')  # prevent GET logout