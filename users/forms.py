from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class UserRegisterForm(UserCreationForm):
    email       = forms.EmailField()
    first_name  = forms.CharField()
    last_name   = forms.CharField()
    employee_id = forms.IntegerField()
    phone       = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'employee_id', 'phone']
