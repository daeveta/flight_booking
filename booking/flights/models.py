from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} profile'


class City(models.Model):
    city = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.city}"


class Airport(models.Model):
    city_airport = models.ForeignKey(City, on_delete=models.CASCADE, related_name='cities', default=None)
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.title}"


class Ticket(models.Model):
    departure_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departure', default=None)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_airport', default=None)
    destination_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='destination', default=None)
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='destination_airport', default=None)
    seats_count = models.IntegerField()
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    # __gt = self.request.GET['dep_date'],
    # __lt = self.request.GET['dep_date']
    price = models.DecimalField(max_digits=8, decimal_places=0)

    def __str__(self):
        return f"{self.id} - {self.departure_city} to {self.destination_city}"
