from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket, Order, Airport, Profile, Flight, Message
from django.forms import Form, PasswordInput, CharField, ModelForm
from django.core.validators import RegexValidator


class LoginForm(Form):
    username = CharField(label='Username')
    password = CharField(label='Password', widget=PasswordInput())


class UserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class SearchForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['departure_city', 'departure_airport', 'destination_city', 'destination_airport', 'departure_date',
                  'arrival_date', 'price']
        widgets = {
            "departure_date": forms.DateInput(attrs={'type': 'date'}, format=settings.DATE_INPUT_FORMATS),
            "arrival_date": forms.DateInput(attrs={'type': 'date'}, format=settings.DATE_INPUT_FORMATS),
            "price": forms.NumberInput(attrs={'type': 'range', 'step': '10', 'min': '50', 'max': '700', 'value': '700', 'id': 'range-field'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departure_airport'].queryset = Airport.objects.none()
        self.fields['destination_airport'].queryset = Airport.objects.none()

        if 'departure_city' in self.data:
            try:
                city_airport_id = int(self.data.get('departure_city'))
                self.fields['departure_airport'].queryset = Airport.objects.filter(city_airport_id=city_airport_id).order_by('title')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['departure_airport'].queryset = self.instance.departure_city.departure_airport_set.order_by('title')

        if 'destination_city' in self.data:
            try:
                city_airport_id = int(self.data.get('destination_city'))
                self.fields['destination_airport'].queryset = Airport.objects.filter(city_airport_id=city_airport_id).order_by('title')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['destination_airport'].queryset = self.instance.destination_city.destination_airport_set.order_by('title')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            "birthday": forms.DateInput(attrs={'type': 'date'}, format=settings.DATE_INPUT_FORMATS),
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email',)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'birthday',)
        widgets = {
            "birthday": forms.DateInput(attrs={'type': 'date'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            "text": forms.Textarea(attrs={'width': '400px', 'cols': '40', 'rows': '4'})
        }
        labels = {
            'text': 'Message:',
        }
