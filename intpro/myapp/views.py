from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Course, Profile, UserCourse
import re



def home(request):
    courses = Course.objects.all()  # Fetch all courses from the database
    return render(request, 'home.html', {'courses': courses})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate inputs
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif not re.match(r'^[789]\d{9}$', phone):
            messages.error(request, "Invalid phone number.")
        elif not re.match(r'^\S+@\S+\.\S+$', email):
            messages.error(request, "Invalid email address.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Create user
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, "Registration successful.")
            return redirect('login')

    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html', {'title': 'Login'})


@login_required
def register_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)

        # Create a record in the UserCourse model
        UserCourse.objects.create(user=request.user, course=course)

        return redirect('course_track')  # Redirect to course track page

    courses = Course.objects.all()  # List all courses
    return render(request, 'courses.html', {'courses': courses})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'title': 'Dashboard'})

@login_required
def course_track(request):
    # Get the courses the user has registered for
    user_courses = UserCourse.objects.filter(user=request.user)
    courses = [user_course.course for user_course in user_courses]

    return render(request, 'course_track.html', {'courses': courses})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)  # Ensure Profile exists

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        profile.mobile_number = request.POST.get('mobile_number')

        new_password = request.POST.get('password')
        if new_password:
            user.password = make_password(new_password)

        user.save()
        profile.save()  # Save Profile changes
        return redirect('profile')  # Redirect to profile page

    return render(request, 'edit_profile.html')


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home') # Redirect to the landing page (initial page)
