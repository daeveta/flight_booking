from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket
from django.forms import Form, PasswordInput, CharField, ModelForm, DateInput


class LoginForm(Form):
    username = CharField(label='Username')
    password = CharField(label='Password', widget=PasswordInput())


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class SearchForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['departure_city', 'departure_airport', 'destination_city', 'destination_airport', 'departure_date',
                  'arrival_date', 'price']
        widgets = {
            "departure_date": DateInput(attrs={'type': 'date'}),
            "arrival_date": DateInput(attrs={'type': 'date'})
        }
