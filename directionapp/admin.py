from django.contrib import admin
from .models import Direction
# Register your models here.

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    pass

