from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TrackingTask


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TrackingTaskForm(forms.ModelForm):
    class Meta:
        model = TrackingTask
        fields = ['input_video', 'model_weight', 'detect_class']
