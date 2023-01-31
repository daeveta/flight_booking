import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from djoser.conf import User

from .forms import UserForm, LoginForm, SearchForm, OrderForm, UserUpdateForm, ProfileUpdateForm
# from .filters import FilterTickets
from django.contrib import messages
# from cart.cart import Cart

from .models import Ticket, Profile, OrderItem, Order, Airport, City


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


@login_required(login_url='/log-in')
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile_edit.html', context)


@login_required(login_url='/log-in')
def ticket_search(request):
    # queryset = Ticket.objects.all()
    queryset1 = Ticket.objects.filter(is_available=True)
    queryset2 = Ticket.objects.filter(is_available=True)
    queryset3 = Ticket.objects.filter(is_available=True)
    queryset4 = Ticket.objects.filter(is_available=True)
    queryset5 = Ticket.objects.filter(is_available=True)
    queryset6 = Ticket.objects.filter(is_available=True)
    queryset7 = Ticket.objects.filter(is_available=True)
    form = SearchForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['departure_city']:
            queryset1 = Ticket.objects.filter(departure_city=form.cleaned_data['departure_city'])
        if form.cleaned_data['departure_airport']:
            queryset2 = Ticket.objects.filter(departure_airport=form.cleaned_data['departure_airport'])
        if form.cleaned_data['destination_city']:
            queryset3 = Ticket.objects.filter(destination_city=form.cleaned_data['destination_city'])
        if form.cleaned_data['destination_airport']:
            queryset4 = Ticket.objects.filter(destination_airport=form.cleaned_data['destination_airport'])
        if form.cleaned_data['departure_date']:
            queryset5 = Ticket.objects.filter(departure_date=form.cleaned_data['departure_date'])
        if form.cleaned_data['arrival_date']:
            queryset6 = Ticket.objects.filter(arrival_date=form.cleaned_data['arrival_date'])
        if form.cleaned_data['price'] or form.cleaned_data['price'] == 0:
            queryset7 = Ticket.objects.filter(price__lte=form.cleaned_data['price'])
    queryset = queryset1 & queryset2 & queryset3 & queryset4 & queryset5 & queryset6 & queryset7
    return render(request, 'ticket_search.html', {"queryset": queryset, "form": form})


def ticket_booking(request, id=None):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            ticket = Ticket.objects.get(pk=id)
            order.ticket = ticket
            order.save()
            instance = Ticket.objects.get(pk=id)
            instance.user = request.user
            instance.is_available = False
            instance.save()
            return render(request, 'ticket_booked.html', {"order": order})
        else:
            form = OrderForm()
            return render(request, 'ticket_booking.html', {'form': form})
    person_instance = User.objects.get(profile=request.user.profile)
    form = OrderForm(instance=person_instance)
    return render(request, 'ticket_booking.html', {'form': form})

    # filters = FilterTickets(request.GET, queryset=queryset)
    #
    # context = {'filters': filters}
    # return render(request, 'ticket_search.html', {"tickets": queryset, "form": form})


def load_airports(request):
    city_airport_id = request.GET.get('city_airport_id')
    airports = Airport.objects.filter(city_airport_id=city_airport_id).all()
    return render(request, 'dropdown_list.html', {'airports': airports})


def booked_tickets(request):
    orders = Order.objects.all().filter(user=request.user)
    return render(request, 'booked_tickets.html', {"orders": orders})


def delete(request, pk):
    order = Order.objects.get(id=pk)
    # instance = Ticket.objects.get(id=pk)
    if request.method == "POST":
        # instance.is_available = True
        # instance.save()
        order.delete()
        return redirect('booked')
    return render(request, 'delete_order.html', {'item': order})