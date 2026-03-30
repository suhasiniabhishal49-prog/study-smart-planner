from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, timezone as dt_timezone
from .models import Subject, Task


# ----- Registration Form -----
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        pw2 = cleaned_data.get('password_confirm')
        if pw and pw2 and pw != pw2:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


# ----- Subject Form -----
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'priority', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Physics, Maths...'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        }


# ----- Task Form -----
class TaskForm(forms.ModelForm):
    # Split deadline into date and time for better control
    deadline_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'id_deadline_date'}),
        required=True,
        label='Deadline Date'
    )
    deadline_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'id': 'id_deadline_time'}),
        required=True,
        initial='09:00',
        label='Deadline Time'
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'subject', 'estimated_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description...'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'estimated_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
        }

    def __init__(self, *args, **kwargs):
        # Only show subjects belonging to the logged-in user
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
        
        # If editing, split the deadline into date and time
        if self.instance and self.instance.deadline:
            # Convert UTC to local time
            local_deadline = timezone.localtime(self.instance.deadline)
            self.fields['deadline_date'].initial = local_deadline.date()
            self.fields['deadline_time'].initial = local_deadline.time()

    def clean(self):
        """Combine date and time into a single datetime in UTC."""
        cleaned_data = super().clean()
        deadline_date = cleaned_data.get('deadline_date')
        deadline_time = cleaned_data.get('deadline_time')
        
        if deadline_date and deadline_time:
            # Combine date and time into a naive datetime
            naive_datetime = datetime.combine(deadline_date, deadline_time)
            
            # Get system's local timezone offset
            offset = datetime.now(dt_timezone.utc).astimezone().utcoffset()
            local_tz = dt_timezone(offset) if offset else dt_timezone.utc
            
            # Make aware with local timezone
            local_datetime = naive_datetime.replace(tzinfo=local_tz)
            
            # Convert to UTC for storage
            utc_datetime = local_datetime.astimezone(dt_timezone.utc)
            
            # Store in cleaned_data as 'deadline' for the model
            cleaned_data['deadline'] = utc_datetime
        
        return cleaned_data

    def save(self, commit=True):
        """Save the task with the combined deadline."""
        deadline = self.cleaned_data.get('deadline')
        if deadline:
            self.instance.deadline = deadline
        return super().save(commit=commit)
