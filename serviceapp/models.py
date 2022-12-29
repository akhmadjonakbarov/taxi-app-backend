from django.db import models
from userapp.models import CustomUser
from directionapp.models import Direction

# Create your models here.
class Service(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    # direction = models.OneToOneField(Direction, on_delete=models.CASCADE ,related_name="direction_q")
    from_where = models.CharField(max_length=250)
    to_where = models.CharField(max_length=250)
    car_type = models.CharField(max_length=250)
    car_images = models.ForeignKey('CarImages', on_delete=models.CASCADE, related_name="car_images")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_services")

    def __str__(self):
        return self.title


class CarImages(models.Model):
    image = models.FileField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.image.name