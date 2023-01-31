import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    phone = models.CharField(default=None, max_length=50, null=True)
    birthday = models.DateField(default=None, name='birthday', null=True)

    def __str__(self):
        return f'{self.user.username} profile'

    # def save(self):
    #     super().save()
    #
    #     img = Image.open(self.image.path)

        # if img.height > 500 or img.width > 500:
        #     output_size = (500, 500)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)


class City(models.Model):
    city = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.city}"


class Airport(models.Model):
    city_airport = models.ForeignKey(City, on_delete=models.CASCADE, related_name='cities')
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.title}"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    departure_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departure', blank=True)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_airport', blank=True)
    destination_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='destination', blank=True)
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='destination_airport', blank=True)
    seats_count = models.IntegerField(blank=True, default=None)
    departure_date = models.DateField(blank=True, null=True, default=None)
    departure_time = models.TimeField(blank=True, null=True, default=None)
    arrival_date = models.DateField(blank=True, null=True, default=None)
    arrival_time = models.TimeField(blank=True, null=True, default=None)
    # __gt = self.request.GET['dep_date'],
    # __lt = self.request.GET['dep_date']
    price = models.DecimalField(max_digits=4, decimal_places=0, blank=True, default=None)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.departure_city} ({self.departure_airport}) — {self.destination_city} ({self.destination_airport}): {self.departure_date}"


class Order(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(default=None, max_length=50, null=True)
    birthday = models.DateField(default=None, name='birthday', null=True)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return 'Order {}'.format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.id)
