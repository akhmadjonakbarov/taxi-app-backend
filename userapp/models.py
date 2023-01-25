from django.contrib.auth.models import AbstractUser

from django.db import models
from rest_framework.authtoken.models import Token as AuthToken


# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=9)
    image = models.FileField(upload_to="profile-image", default="profile-image/collage.jpg")

    def __str__(self):
        return self.username

    def get_services(self):
        return self.user_services.all()


