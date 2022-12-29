from django.db import models

# Create your models here.
class Direction(models.Model):
    direction = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.direction
    
    