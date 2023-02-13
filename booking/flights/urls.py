from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('sign-up/', views.sign_up, name='signup'),
    path('log-in/', views.log_in, name='login'),
    path('log-out/', views.log_out, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    path('search/', views.ticket_search, name='search'),
    path('booking/<int:id>', views.ticket_booking, name='booking-ticket'),
    path('booked/', views.ticket_booking, name='booked-ticket'),
    path('ajax/load-airports/', views.load_airports, name='ajax_load_airports'),
    path('edit/', views.edit_profile, name='edit-profile'),
    path('booked-tickets/', views.booked_tickets, name='booked'),
    path('delete_order/<str:pk>', views.delete, name='delete'),
    path('messages/', views.message_for_admin, name='messages'),
    path('messages-list/', views.admin_message_list, name='admin-list'),
    path('chat/<int:id>', views.chat, name='chat')
]
