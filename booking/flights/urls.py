from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('sign-up', views.sign_up, name='signup'),
    path('log-in', views.log_in, name='login'),
    path('log-out', views.log_out, name='logout'),
    path('profile', views.profile_page, name='profile'),
    path('search', views.ticket_search, name='search')
]
