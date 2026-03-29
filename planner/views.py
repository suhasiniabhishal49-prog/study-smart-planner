from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, Value, IntegerField

from .models import Subject, Task
from .forms import UserRegistrationForm, SubjectForm, TaskForm


# =============================================================================
# AUTHENTICATION VIEWS
# =============================================================================

def home(request):
    """Landing page – redirect authenticated users straight to dashboard."""
    if request.user.is_authenticated:
        return redirect('planner:dashboard')
    return render(request, 'planner/home.html')


def register(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('planner:dashboard')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('planner:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'planner/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('planner:dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('planner:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'planner/login.html', {'form': form})


def logout_view(request):
    """Log out the user and redirect to login page."""
    logout(request)
    return redirect('planner:login')


# =============================================================================
# DASHBOARD
# =============================================================================

@login_required
def dashboard(request):
    """Main dashboard with stats, today's tasks and upcoming deadlines."""
    today = timezone.localtime().date()
    all_tasks = Task.objects.filter(user=request.user)

    completed_tasks = all_tasks.filter(status='Completed').count()
    pending_tasks_qs = all_tasks.filter(status='Pending')
    overdue_tasks = pending_tasks_qs.filter(deadline__lt=timezone.now())
    today_tasks = pending_tasks_qs.filter(deadline__date=today)
    upcoming_tasks = pending_tasks_qs.filter(deadline__gte=timezone.now()).order_by('deadline')[:5]

    context = {
        'total_tasks': all_tasks.count(),
        'completed_tasks': completed_tasks,
        'pending_count': pending_tasks_qs.count(),
        'overdue_tasks': overdue_tasks,
        'today_tasks': today_tasks,
        'upcoming_tasks': upcoming_tasks,
    }
    return render(request, 'planner/dashboard.html', context)


# =============================================================================
# PROFILE
# =============================================================================

@login_required
def profile(request):
    """Show user profile and account stats."""
    total_tasks = Task.objects.filter(user=request.user).count()
    completed = Task.objects.filter(user=request.user, status='Completed').count()
    subjects_count = Subject.objects.filter(user=request.user).count()
    context = {
        'total_tasks': total_tasks,
        'completed': completed,
        'pending': total_tasks - completed,
        'subjects_count': subjects_count,
    }
    return render(request, 'planner/profile.html', context)


# =============================================================================
# SUBJECTS
# =============================================================================

@login_required
def subjects(request):
    """List of all subjects for the logged-in user."""
    subs = Subject.objects.filter(user=request.user)
    return render(request, 'planner/subjects.html', {'subjects': subs})


@login_required
def add_subject(request):
    """Add a new subject."""
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect('planner:subjects')
    else:
        form = SubjectForm()
    return render(request, 'planner/add_subject.html', {'form': form})


@login_required
def delete_subject(request, subject_id):
    """Delete a subject and all its tasks."""
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    if request.method == 'POST':
        subject.delete()
        return redirect('planner:subjects')
    return render(request, 'planner/confirm_delete.html', {
        'item': subject, 'item_type': 'Subject', 'cancel_url': 'planner:subjects'
    })


# =============================================================================
# TASKS
# =============================================================================

@login_required
def tasks_view(request):
    """View all tasks with optional search and subject filter."""
    tasks = Task.objects.filter(user=request.user).order_by('deadline')
    subjects_list = Subject.objects.filter(user=request.user)

    search_query = request.GET.get('search', '').strip()
    subject_filter = request.GET.get('subject', '')

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)
    if subject_filter:
        tasks = tasks.filter(subject__id=subject_filter)

    return render(request, 'planner/tasks.html', {
        'tasks': tasks,
        'subjects': subjects_list,
        'search_query': search_query,
        'selected_subject': subject_filter,
    })


@login_required
def add_task(request):
    """Add a new task."""
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('planner:tasks')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'planner/add_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    """Edit an existing task."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('planner:tasks')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'planner/add_task.html', {'form': form, 'editing': True, 'task': task})


@login_required
def delete_task(request, task_id):
    """Delete a task with confirmation."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('planner:tasks')
    return render(request, 'planner/confirm_delete.html', {
        'item': task, 'item_type': 'Task', 'cancel_url': 'planner:tasks'
    })


@login_required
def toggle_task_status(request, task_id):
    """Toggle a task between Pending and Completed."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.status = 'Completed' if task.status == 'Pending' else 'Pending'
        task.save()
    # Go back to wherever the user was (dashboard or tasks page)
    return redirect(request.META.get('HTTP_REFERER', 'planner:tasks'))


# =============================================================================
# SCHEDULE (Smart Planner)
# =============================================================================

@login_required
def schedule(request):
    """
    Smart scheduler: auto-assign pending tasks to days based on
    available daily study minutes (priority + deadline ordered).
    """
    try:
        daily_minutes = max(30, int(request.GET.get('minutes', 120)))
    except ValueError:
        daily_minutes = 120

    # Annotate priority weight for ordering
    pending_tasks = Task.objects.filter(user=request.user, status='Pending').annotate(
        priority_weight=Case(
            When(subject__priority='High', then=Value(1)),
            When(subject__priority='Medium', then=Value(2)),
            When(subject__priority='Low', then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        )
    ).order_by('deadline', 'priority_weight')

    # Build daily plan list
    schedule_plan = []
    current_day = timezone.localtime().date()
    current_day_minutes = 0
    day_tasks = []

    for task in pending_tasks:
        remaining = task.estimated_time
        while remaining > 0:
            available = daily_minutes - current_day_minutes
            if available <= 0:
                if day_tasks:
                    schedule_plan.append({'date': current_day, 'tasks': day_tasks})
                current_day += timedelta(days=1)
                current_day_minutes = 0
                day_tasks = []
                available = daily_minutes

            chunk = min(remaining, available)
            day_tasks.append({'task': task, 'allocated': chunk})
            current_day_minutes += chunk
            remaining -= chunk

    if day_tasks:
        schedule_plan.append({'date': current_day, 'tasks': day_tasks})

    return render(request, 'planner/schedule.html', {
        'schedule_plan': schedule_plan,
        'daily_minutes': daily_minutes,
    })


# =============================================================================
# CALENDAR VIEW
# =============================================================================

@login_required
def calendar_view(request):
    """Show tasks filtered by today / week / all."""
    sort_by = request.GET.get('sort', 'today')
    tasks = Task.objects.filter(user=request.user).order_by('deadline')

    if sort_by == 'today':
        tasks = tasks.filter(deadline__date=timezone.localtime().date())
    elif sort_by == 'week':
        today = timezone.localtime().date()
        tasks = tasks.filter(deadline__date__gte=today, deadline__date__lte=today + timedelta(days=7))

    return render(request, 'planner/calendar.html', {'tasks': tasks, 'sort_by': sort_by})


# =============================================================================
# PROGRESS / ANALYTICS
# =============================================================================

@login_required
def progress_view(request):
    """Show overall stats and per-subject progress bars."""
    tasks = Task.objects.filter(user=request.user)
    total = tasks.count()
    completed = tasks.filter(status='Completed').count()
    pending = total - completed
    overdue = tasks.filter(status='Pending', deadline__lt=timezone.now()).count()
    progress_pct = round((completed / total * 100), 1) if total > 0 else 0

    subjects = Subject.objects.filter(user=request.user)
    subject_stats = []
    for sub in subjects:
        sub_tasks = tasks.filter(subject=sub)
        t = sub_tasks.count()
        c = sub_tasks.filter(status='Completed').count()
        subject_stats.append({
            'subject': sub,
            'total': t,
            'completed': c,
            'percent': round(c / t * 100) if t > 0 else 0,
        })

    return render(request, 'planner/progress.html', {
        'total': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue,
        'progress_pct': progress_pct,
        'subject_stats': subject_stats,
    })
