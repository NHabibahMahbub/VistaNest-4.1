from django.contrib import admin
from .models import Platform, Bid, Favorite

# Register your models here.
admin.site.register(Platform)
admin.site.register(Bid)
admin.site.register(Favorite)
