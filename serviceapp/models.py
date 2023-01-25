from django.db import models
from userapp.models import CustomUser


# Create your models here.
class Service(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_services")
    phone_number = models.CharField(max_length=12)
    from_where = models.CharField(max_length=250)
    to_where = models.CharField(max_length=250)
    leaving_time = models.DateTimeField()
    service_price = models.FloatField()
    car_type = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number
