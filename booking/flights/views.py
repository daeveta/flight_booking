
from datetime import date

from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from djoser.conf import User
from .forms import UserForm, LoginForm, SearchForm, OrderForm, UserUpdateForm, ProfileUpdateForm, MessageForm
from django.contrib import messages


from .models import Ticket, Profile, Airport, City, Flight, Message


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
            user = form.cleaned_data.get('first_name')
            messages.success(request, 'Your profile is created,' + ' ' + user)
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
    return render(request, 'profile.html')


@login_required(login_url='/log-in')
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile is updated successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile_edit.html', context)


def ticket_search(request):
    queryset = Flight.objects.filter(is_available=True).filter(departure_date__gte=date.today())
    form = SearchForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['departure_city']:
            queryset = queryset.filter(departure_city=form.cleaned_data['departure_city'])
        if form.cleaned_data['departure_airport']:
            queryset = queryset.filter(departure_airport=form.cleaned_data['departure_airport'])
        if form.cleaned_data['destination_city']:
            queryset = queryset.filter(destination_city=form.cleaned_data['destination_city'])
        if form.cleaned_data['destination_airport']:
            queryset = queryset.filter(destination_airport=form.cleaned_data['destination_airport'])
        for flight in queryset:
            if flight.departure_date > date.today() or flight.departure_date == date.today():
                if form.cleaned_data['departure_date']:
                    queryset = queryset.filter(departure_date=form.cleaned_data['departure_date'])
        for flight in queryset:
            if flight.arrival_date > flight.departure_date or flight.arrival_date == flight.departure_date:
                if form.cleaned_data['arrival_date']:
                    queryset = queryset.filter(arrival_date=form.cleaned_data['arrival_date'])
        if form.cleaned_data['price'] or form.cleaned_data['price'] == 0:
            queryset = queryset.filter(price__lte=form.cleaned_data['price'])
    return render(request, 'ticket_search.html', {"queryset": queryset, "form": form})


@login_required(login_url='/log-in')
def ticket_booking(request, id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.flight = Flight.objects.get(pk=id)
            if ticket.flight.seats_count > 0:
                ticket.flight.seats_count -= 1
                ticket.flight.update_seats()
            else:
                messages.error(request, 'Error! There is no seats on this flight')
                ticket.flight.update_seats()
                return redirect('search')
            ticket.user = request.user
            ticket.save()
            ticket.flight.save()
            return render(request, 'ticket_booked.html', )
        else:
            form = OrderForm()
            return render(request, 'ticket_booking.html', {'form': form})
    person_instance = User.objects.get(profile=request.user.profile)
    form = OrderForm(instance=person_instance)
    return render(request, 'ticket_booking.html', {'form': form})


def load_airports(request):
    city_airport_id = request.GET.get('city_airport_id')
    airports = Airport.objects.filter(city_airport_id=city_airport_id).all()
    return render(request, 'dropdown_list.html', {'airports': airports})


def booked_tickets(request):
    ticket = Ticket.objects.all().filter(user=request.user)
    return render(request, 'booked_tickets.html', {"ticket": ticket})


def delete(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket_flight = ticket.flight
    if request.method == "POST":
        ticket.delete()
        ticket_flight.seats_count += 1
        ticket_flight.update_seats()
        return redirect('booked')
    return render(request, 'delete_order.html', {'item': ticket})


def message_for_admin(request):
    sender = request.user
    recipient = User.objects.get(id=1)
    message_list = Message.objects.filter(Q(sender=sender) | Q(recipient=sender))
    if request.method == "POST":
        form = MessageForm(request.POST)
        message = form.save(commit=False)
        message.sender = sender
        message.recipient = recipient
        message.save()
    else:
        form = MessageForm()
    return render(request, 'message_for_admin.html',
                  {"message_list": message_list, "form": form, "sender": sender, "recipient": recipient})


def admin_message_list(request):
    message_list = Message.objects.values('sender_id__first_name', 'sender_id').annotate(recipient_messages=Count('sender'))
    return render(request, 'admin_message_list.html', {"message_list": message_list})


def chat(request, id):
    sender = request.user
    recipient = User.objects.get(id=id)
    message_list = Message.objects.filter(Q(sender=recipient) | Q(recipient=recipient))
    if request.method == "POST":
        # import pdb; pdb.set_trace()
        form = MessageForm(request.POST)
        message = form.save(commit=False)
        message.sender = sender
        message.recipient = recipient
        message.save()
    else:
        form = MessageForm()
    return render(request, 'message_for_admin.html', {"message_list": message_list, "form": form})
