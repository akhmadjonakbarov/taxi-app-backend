from django.contrib import admin
from .models import Service, CarImages


# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', ]


@admin.register(CarImages)
class CarImagesAdmin(admin.ModelAdmin):
    pass
