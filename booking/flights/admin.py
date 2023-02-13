from django.contrib import admin
from .models import Profile, City, Airport, Ticket, Order, Flight, Message


admin.site.register(Profile)
admin.site.register(City)
admin.site.register(Airport)
admin.site.register(Ticket)
admin.site.register(Order)
admin.site.register(Flight)
admin.site.register(Message)

# Register your models here.
