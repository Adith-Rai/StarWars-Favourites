from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

#Registration and Login
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#Import API methods
from . planetsAPI import planetsAPI
from . filmsAPI import filmsAPI
from . userFavourites import userFavourites



#HOME
def say_hello_template(request):
    return render(request, 'index.html', { "name":"You"})

#Searches 

#search
@login_required(login_url='/login/')
def search(request):
    
    #Searches are sent as POST requests
    if request.method == 'POST':
        #retrieve search query
        query = request.POST['searchQuery']
    
        apiPlanet = planetsAPI(request)
        apiMovies = filmsAPI(request)
        apiFav = userFavourites(request)
        
        #search planets
        planetResults = apiPlanet.search(query)        
        # If API URL Could not be resolved, return error in dict
        if len(planetResults)!=0 and "error" in planetResults[0]:
            planetResults = []
        #Remove Favourite items retrieved
        planetResults = remove_is_favourite(planetResults)
        
        #search movies
        movieResults = apiMovies.search(query)
        # If API URL Could not be resolved, return error in dict
        if len(movieResults)!=0 and "error" in movieResults[0]:
            movieResults = []
        #Remove Favourite items retrieved
        movieResults = remove_is_favourite(movieResults)
        
        #combine movie and planet results
        combinedResults = movieResults + planetResults
        
        #search favourites
        favouriteResults = apiFav.search(query)
        
        #Remove duplicates and combine with favourites
        results = []
        if (len(favouriteResults)>0) and (len(combinedResults)>0):
            results = remove_duplicates(favouriteResults, combinedResults)        
        elif len(favouriteResults)>0:
            results = favouriteResults
        elif len(combinedResults)>0:
            results = combinedResults
        
        #If error when retrieving data
        if len(results) == 0:
            messages.info(request, 'No Data was found')
            return redirect("/search/")
        elif "error" in results[0]:
            messages.info(request, results[0]["error"])
            return redirect("/search/")
    
        return render(request, 'search.html', { "results": results })
    
    #If GET return blank search
    else:
        messages.info(request, 'No Data was found')
        return render(request, 'search.html')
        

#search favourites
@login_required(login_url='/login/')
def favourites_search(request):
    
    #Searches are sent as POST requests
    if request.method == 'POST':
        #retrieve search query
        query = request.POST['searchQuery']
    
        apiFav = userFavourites(request)
        
        #search favourites
        results = apiFav.search(query)
        
        #If error when retrieving data
        if len(results) == 0:
            messages.info(request, 'No Data was found')
            return redirect("/search/")
        elif "error" in results[0]:
            messages.info(request, results[0]["error"])
            return redirect("/search/")
    
        return render(request, 'search.html', { "results": results })
    
    #If GET return blank search
    else:
        messages.info(request, 'No Data was found')
        return render(request, 'search.html')


#search planets
@login_required(login_url='/login/')
def planet_search(request):
    
    #Searches are sent as POST requests
    if request.method == 'POST':
        #retrieve search query
        query = request.POST['searchQuery']
    
        apiPlanet = planetsAPI(request)
        apiFav = userFavourites(request)
        
        #search planets
        planetResults = apiPlanet.search(query)
        # If API URL Could not be resolved, return error in dict
        if len(planetResults)!=0 and "error" in planetResults[0]:
            planetResults = []
        #Remove Favourite items retrieved
        planetResults = remove_is_favourite(planetResults)
        
        #search favourites
        favouriteResults = apiFav.search(query)
        #filter for only planets
        for i in favouriteResults:
            if i["type"].strip().upper()!="PLANET":
                favouriteResults.remove(i)
        
        #Remove duplicates and combine with favourites
        results = []
        if (len(favouriteResults)>0) and (len(planetResults)>0):
            results = remove_duplicates(favouriteResults, planetResults)        
        elif len(favouriteResults)>0:
            results = favouriteResults
        elif len(planetResults)>0:
            results = planetResults
        
        #If error when retrieving data
        if len(results) == 0:
            messages.info(request, 'No Data was found')
            return redirect("/search/")
        elif "error" in results[0]:
            messages.info(request, results[0]["error"])
            return redirect("/search/")
    
        return render(request, 'search.html', { "results": results })
    
    #If GET return blank search
    else:
        messages.info(request, 'No Data was found')
        return render(request, 'search.html')




#search films
@login_required(login_url='/login/')
def movie_search(request):
    
    #Searches are sent as POST requests
    if request.method == 'POST':
        
        #retrieve search query
        query = request.POST['searchQuery']
    
        apiMovies = filmsAPI(request)
        apiFav = userFavourites(request)
        
        #search movies
        movieResults = apiMovies.search(query)
        # If API URL Could not be resolved, return error in dict
        if len(movieResults)!=0 and "error" in movieResults[0]:
            movieResults = []          
        #Remove Favourite items retrieved
        movieResults = remove_is_favourite(movieResults)
        
        #search favourites
        favouriteResults = apiFav.search(query)
        #filter for only films
        for i in favouriteResults:
            if i["type"].strip().upper()!="FILM":
                favouriteResults.remove(i)
        
        #Remove duplicates and combine with favourites
        results = []
        if (len(favouriteResults)>0) and (len(movieResults)>0):
            results = remove_duplicates(favouriteResults, movieResults)        
        elif len(favouriteResults)>0:
            results = favouriteResults
        elif len(movieResults)>0:
            results = movieResults
        
        #If error when retrieving data
        if len(results) == 0:
            messages.info(request, 'No Data was found')
            return redirect("/search/")
        elif "error" in results[0]:
            messages.info(request, results[0]["error"])
            return redirect("/search/")
    
        return render(request, 'search.html', { "results": results })
    
    #If GET return blank search
    else:
        messages.info(request, 'No Data was found')
        return render(request, 'search.html')



#Resources API - Planets, Movies

# api to films
@login_required(login_url='/login/')
def films_page(request):
    
    api = filmsAPI(request)
    
    movies = api.getAllMoviesData()
    
    #If error when retrieving data
    if len(movies) == 0:
        messages.info(request, 'No Data was found')
        return redirect("/")
    elif "error" in movies[0]:
        messages.info(request, movies[0]["error"])
        return redirect("/")
    
    return render(request, 'movies.html', {"resources":movies , "type":"FILM"})



#api to film
def single_film_page(request):
    
    #Request sent as post
    if request.method == 'POST':
        
        url = request.POST["film_url"].strip()
        #Make sure URL is for a film
        if (url.strip()).find("films") < 0:
            messages.info(request, "Invalid URL")
            return redirect("/films/")
        
        #Check if favourite, convert to bool
        favourite = True
        if len(request.POST["film_favourite"])>0:
            fav = request.POST["film_favourite"]
            if fav.strip() == "False":
                favourite = False
            else:
                favourite = True

        
        api = filmsAPI(request)
        
        #Get Data of Film in url
        film = api.getSingleMovieData(url)
        
        #If error when retrieving data
        if len(film) == 0:
            messages.info(request, 'No Data was found')
            return redirect("/films/")
        elif "error" in film:
            messages.info(request, film["error"])
            return redirect("/films/")
        
        #render the film page
        return render(request, 'movie.html', {"film":film, "type":"FILM", "favourite": favourite})   
    
    #If GET, go to films page
    else:
        return redirect("/films/")

# api to planets
@login_required(login_url='/login/')
def planets_page(request):
    
    api = planetsAPI(request)
    
    planets = api.getAllPlanetsData()
    
    #If error when retrieving data
    if len(planets) == 0:
        messages.info(request, 'No Data was found')
        return redirect("/")
    elif "error" in planets[0]:
        messages.info(request, planets[0]["error"])
        return redirect("/")
    
    return render(request, 'planets.html', {"resources":planets, "type":"PLANET"})


#api to planet
@login_required(login_url='/login/')
def single_planet_page(request):
    
    #Request sent as post
    if request.method == 'POST':
        
        url = request.POST["planet_url"].strip()
        
        #Check if favourite, convert to bool
        favourite = True
        if len(request.POST["planet_favourite"])>0:
            fav = request.POST["planet_favourite"]
            if fav.strip() == "False":
                favourite = False
            else:
                favourite = True

        #Make sure URL is for a planet
        if (url.strip()).find("planets") < 0:
            messages.info(request, "Invalid URL")
            return redirect("/planets/")
        
        api = planetsAPI(request)
        
        #Get Data of Planet in url
        planet = api.getSinglePlanetData(url)
        
        #If error when retrieving data
        if len(planet) == 0:
            messages.info(request, 'No Data was found')
            return redirect("/planets/")
        elif "error" in planet:
            messages.info(request, planet["error"])
            return redirect("/planets/")
        
        #render the planet page
        return render(request, 'planet.html', {"planet":planet, "type":"PLANET", "favourite": favourite})   
    
    #If GET, go to planets page
    else:
        return redirect("/planets/")



#Favourites API

#get favourites
@login_required(login_url='/login/')
def favourites_page(request):

    api = userFavourites(request)
    
    favourites = api.getAllFavouritesList()
    
    return render(request, 'favourites.html', {"resources":favourites})

#add to favourites
#Add to db
@login_required(login_url='/login/')
def add_favourites(request):
    
    if request.method == 'POST':
        
        #If name has already been entered
 
        api = userFavourites(request)
        
        #If name enteed was blank, save as resource name
        name = request.POST["name"].strip()
        if len(name)==0:
            name = request.POST["resource_name"]
            
        #Add to favourites
        added = api.addFavourite(
            name, 
            request.POST["resource_name"].strip(), 
            request.POST["resource_type"].strip(), 
            request.POST["resource_url"].strip()
        )
        
        #check for success
        if added == 0:
            messages.info(request, "Error adding to favourites, item not added")
            return redirect("/favourites-add/")
        elif added == -1:
            messages.info(request, "Item already present in favourites")
            return render(request, "favourites-add.html", {
                "favourite":{
                    "resource_name":request.POST['resource_name'], 
                    "resource_type":request.POST['resource_type'], 
                    "resource_url": request.POST['resource_url']
                    }
                }
            )
        #successfully added
        else:
            return redirect('/favourites/')
 
    #Direct access through URL redirects to Home
    else:
        return redirect('/')
    
    
#Render Add to Favourites page - enter custom name
@login_required(login_url='/login/')
def add_favourites_page(request):
    
    if request.method == 'POST':
        
        favourite = {
                "resource_name": request.POST['resource_name'], 
                "resource_type": request.POST['resource_type'], 
                "resource_url": request.POST['resource_url']
        }
        
        return render(request, "favourites-add.html", {"favourite": favourite})  
    
    #Direct access through URL redirects to Home
    else:
        return redirect('/')


#Rename Favourite in DB
@login_required(login_url='/login/')
def rename_favourites(request):
    
    if request.method == 'POST':
        
        #If name has already been entered
 
        api = userFavourites(request)
        
        #If name enteed was blank, save as resource name
        name = request.POST["new_name"].strip()
        if len(name)==0:
            name = request.POST["favourite_name"]
            
        #Add to favourites
        renamed = api.renameFavourite(
            name, 
            request.POST["favourite_name"].strip(), 
            request.POST["resource_type"].strip(), 
            request.POST["resource_url"].strip()
        )
        
        #check for success
        if renamed == 0:
            messages.info(request, "Error renaming favourites, item not renamed")
            return redirect("/favourites-add/")
        elif renamed == -1:
            messages.info(request, "name already present in favourites, please use different name")
            return render(request, "favourites-rename.html", {
                "favourite":{
                    "favourite_name":request.POST['favourite_name'], 
                    "resource_type":request.POST['resource_type'], 
                    "resource_url": request.POST['resource_url']
                    }
                }
            )
        #successfully added
        else:
            return redirect('/favourites/')
 
    #Direct access through URL redirects to Home
    else:
        return redirect('/')
    
    
#Render Rename Favourites page - enter new name
@login_required(login_url='/login/')
def rename_favourites_page(request):
    
    if request.method == 'POST':
        
        favourite = {
                "favourite_name": request.POST['favourite_name'], 
                "resource_type": request.POST['resource_type'], 
                "resource_url": request.POST['resource_url']
        }
        
        return render(request, "favourites-rename.html", {"favourite": favourite})  
    
    #Direct access through URL redirects to Home
    else:
        return redirect('/')


#Delete from Favourites
@login_required(login_url='/login/')
def delete_favourite(request):
 
    if request.method == 'POST':
        #If name has already been entered
     
        api = userFavourites(request)
            
        #Delete from favourites
        deleted = api.deleteFavourite(
            request.POST["favourite_name"].strip(), 
            request.POST["resource_type"].strip(), 
            request.POST["resource_url"].strip()
        )
        
        #check for success
        if deleted == 0:
            messages.info(request, "Error deleting favourite, item not deleted")
            return redirect("/favourites-add/")

        #successfully deleted
        else:
            return redirect('/favourites/')
     
    #Direct access through URL redirects to Home
    else:
        return redirect('/')



#Accounts

#account login
def login(request):

    #if Submit values - so POST Request
    if request.method == 'POST':
        
        #Retrieve form fields
        username = request.POST['USER_NAME']
        password = request.POST['PASSWORD']
        
        #check if fields are empty
        if len(username.strip())==0:
            messages.info(request, 'Please Enter Username')
            return redirect("/login/")
        elif len(password.strip())==0:
            messages.info(request, 'Please Enter Password')
            return redirect("/login/")
        
        #check if user exists with correct password
        user = auth.authenticate(username=username,password=password)
        
        #if username or password is wrong, show error message in page
        if user is None:
            messages.info(request, 'Invalid Credentials')
            return redirect("login")
        
        #if username or password is correct and matches, log user in
        else:
            auth.login(request, user)
            messages.info(request, username+ ' is now Logged In!')

            
        #On successful Login, go to home page
        return redirect("/")
    
    #If we are trying to reach/ retrieve login page - so GET Request
    else:
        return render(request, 'login.html')
    
    
    

#account logout
@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect('/')

    
#accounts register
def register(request):

    #if Submit values - so POST Request
    if request.method == 'POST':
        
        #Retrieve form fields
        username = request.POST['USER_NAME']
        password = request.POST['PASSWORD']
        confirm_password = request.POST['PASSWORD_CONFIRM']
        
        #check if fields are empty
        if len(username.strip())==0:
            messages.info(request, 'Please Enter Username')
            return redirect("/register/")
        elif len(password.strip())==0:
            messages.info(request, 'Please Enter Password')
            return redirect("/register/")
        
        #if password and confirm password match
        if password == confirm_password: 
            
            #if username already exists, send message
            if User.objects.filter(username=username):
                messages.info(request, 'Username already in use')
                return redirect("/login/")
            
            #if usrename is new/unique and password matches confirm password, register user in auth_user table
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.info(request, 'User Created!')
                
        # If password does Not match conform password, display error message
        else:
            messages.info(request, 'Confirmed Password does Not match')
            return redirect("/register/")
            
        #On successful entering to DB, go to login page
        return redirect("/login/")
    
    #If we are only trying to reach/retrieve the registration page - so GET Request
    else:
        return render(request, 'register.html')
    
    
#______________________________________________________________________________________________________________________#

##Utility functions

#Utility to remove duplicates from list
def remove_duplicates(l1, l2):
      
    temp = l2
    
    for i in l1:
        for j in temp:
            if "name" in j:
                if i["name"].strip() == j["name"].strip():
                    l2.remove(j)
            else:
                if i["name"].strip() == j["title"].strip():
                    l2.remove(j)
    return l1 + l2


#Utility to remove is_favourite items
def remove_is_favourite(data):
    
    tmp = data
    
    for i in tmp:
        if i["is_favourite"]==True:
            data.remove(i)
            
    return data