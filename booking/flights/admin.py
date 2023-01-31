from django.contrib import admin
from .models import Profile, City, Airport, Ticket, Order


admin.site.register(Profile)
admin.site.register(City)
admin.site.register(Airport)
admin.site.register(Ticket)
admin.site.register(Order)

# Register your models here.
