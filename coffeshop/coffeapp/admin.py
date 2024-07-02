from django.contrib import admin

from .models import Orders, Products, Admins, User ,Users

admin. site.register(User)
admin. site.register(Users)
admin. site.register(Orders)
admin. site.register(Products)
admin. site.register(Admins)

# Register your models here.
