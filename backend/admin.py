from django.contrib import admin
from . models import Favourites

# Register User and Favourite Tables for admin access
admin.site.register(Favourites)