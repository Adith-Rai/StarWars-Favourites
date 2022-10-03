from django.db import models

#Users Table
from django.contrib.auth.models import User

# Create your models here.
#Models will represent Favourites Table in general
    

#Contains all favouries for all users
# if star wars data was in a DB as well, we would use many-to-many relation
# Favourites table has user, name given, true name/title and API url
class Favourites(models.Model):
    ID = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='FAVOURITES_ID')
    NAME = models.CharField(max_length=100) 
    RESOURCE_NAME = models.CharField(max_length=100, default="unknown")
    RESOURCE_TYPE = models.CharField(max_length=100, default="unknown") 
    ACCOUNT = models.ForeignKey(User, on_delete=models.CASCADE) 
    URL = models.CharField(max_length=150, default="https://swapi.dev/api/") 
    