from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from .decorators import unauthenticated_user

User = get_user_model()

@unauthenticated_user('home')
def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Validation
        if not all([email, role, password, password2]):
            messages.error(request, "All fields are required")
            return redirect("signup")

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')
        
        if role not in ['job_seeker', 'employer']:
            messages.error(request, "Invalid account type selected")
            return redirect("signup")

        # Create user
        user = User.objects.create_user(
            email=email,
            role=role,
            password=password,
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'accounts/signup.html')

@unauthenticated_user('home')
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('login')

    return redirect('home')  # prevent GET logout