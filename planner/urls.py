from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    # --- Public pages ---
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # --- Main app pages (login required) ---
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('progress/', views.progress_view, name='progress'),
    path('schedule/', views.schedule, name='schedule'),
    path('calendar/', views.calendar_view, name='calendar'),

    # --- Subjects ---
    path('subjects/', views.subjects, name='subjects'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),

    # --- Tasks ---
    path('tasks/', views.tasks_view, name='tasks'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('tasks/toggle/<int:task_id>/', views.toggle_task_status, name='toggle_task_status'),
]
