from django.db import models
from userapp.models import CustomUser


# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=250)
    car_number = models.CharField(max_length=250)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_cars")

    def __str__(self) -> str:
        return str(self.name)

