from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, LoginForm, SearchForm
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


@login_required(login_url='/log-in')
def about(request):
    return render(request, 'about.html')


def sign_up(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # user = form.cleaned_data.get('first_name')
            # messages.success(request, 'Congratulations!' + user)
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'sign_up.html', {'form': form})


def log_in(request):
    error = ''
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(password=data['password'], username=data['username'])
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                return redirect('login')
        else:
            error = 'ERROR!'
    else:
        form = LoginForm()
    return render(request, 'log_in.html', {
        'form': form,
        'error': error,
    })


def log_out(request):
    logout(request)
    return redirect('home')


@login_required
def profile_page(request):
    return render(request, 'profile.html') # сигналы для того чтобы профиль создавался автоматически


def ticket_search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            search_data = authenticate(departure_city=data['form.dep_city'], departure_airport=data['form.dep_airport'],
                                       destination_city=data['form.dest_city'], destination_airport=data['form.dest_airport'],
                                       departure_date=data['form.dep_date'], arrival_date=data['form.arr_date'], price=data['form.price'])
            if search_data is not None:
                render(request, search_data)
                return redirect('home')
            else:
                return redirect('login-me')
    else:
        form = SearchForm()
        context = {
            'form': form,
            }
        return render(request, 'ticket_search.html', context)



