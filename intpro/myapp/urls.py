from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.login_user, name='login'),  # Login page
    path('courses/', views.register_course, name='register_course'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('course_track/', views.course_track, name='course_track'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout, name='logout'),
]
