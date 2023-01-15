from django.contrib import admin
from .models import Profile, City, Airport, Ticket


admin.site.register(Profile)
admin.site.register(City)
admin.site.register(Airport)
admin.site.register(Ticket)

# Register your models here.
