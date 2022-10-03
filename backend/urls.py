from django.urls import path
from . import views

# URL CONF
urlpatterns = [
    
    #Home
    path('', views.say_hello_template, name='home'), #HOME PAGE
    
    #Accounts
    path('register/', views.register, name='register'), #Register Page
    path('login/', views.login, name='login'), #Login Page
    path('logout', views.logout, name='logout'), #Log out

    #Planets
    path('planets/', views.planets_page, name="planets"), #Planets List
    path('planets/planet/', views.single_planet_page, name="planet-page"), #Single Planet Data
    
    #Films
    path('films/', views.films_page, name="films"), #Films List
    path('films/film/', views.single_film_page, name="film-page"), #Single Film Data
    
    #Favourites
    path('favourites/', views.favourites_page, name="favourites"), #Favourites List
    path('favourites-add/', views.add_favourites_page, name="favourites-add"), #Add to Favourites List Page
    path('favourites-adding/', views.add_favourites, name="favourites-adding"), #Processing Add, No Page
    path('favourites-deleting/', views.delete_favourite, name="favourites-deleteing"), #Processing Delete
    path('favourites-rename/', views.rename_favourites_page, name="favourites-rename"), #Add to Favourites List Page
    path('favourites-renaming/', views.rename_favourites, name="favourites-rename"), #Processing Add, No Page
       
    #Search
    path('search/', views.search, name='search'), #SEARCH
    path('planets/search/', views.planet_search, name='planets-search'), #PLANET SEARCH
    path('films/search/', views.movie_search, name='films-search'), #FILMS SEARCH
    path('favourites/search/', views.favourites_search, name='favourites-search'), #FAVOURITES SEARCH
    
]