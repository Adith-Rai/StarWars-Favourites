#For search query prep
import re

# To read config file
from . models import Favourites


#Functionality for Favourites API
class userFavourites:
    
  # Do nothing
  def __init__(self, request):
    self.request = request
    
    
    
    
  # get All favourites
  def getAllFavouritesList(self):
      
      #retrieve all favourites of this user
      favs = Favourites.objects.filter(ACCOUNT=self.request.user)

      #empty list if no results
      if favs is None:
          return []
      
      #put retrieved items in list of dicts
      listFavs = []
      for fav in favs:
          listFavs.append({"name" : fav.NAME, "resource" : fav.RESOURCE_NAME, "url" : fav.URL, "type" : fav.RESOURCE_TYPE})
      
      return listFavs
  

  #get Movie favouritse
  def getFavouriteFilmsList(self):
      
      #retrieve all favourites films of this user
      favs = Favourites.objects.filter(ACCOUNT=self.request.user, RESOURCE_TYPE="FILM")
      
      #empty list if no results
      if favs is None:
          return []
      
      #put retrieved items in list of dicts
      listFavs = []
      for fav in favs:
          listFavs.append({"name" : fav.NAME, "resource" : fav.RESOURCE_NAME, "type" : fav.RESOURCE_TYPE, "url" : fav.URL})
      
      return listFavs
  
    
  #get favourite planets
  def getFavouritePlanetsList(self):
      
      #retrieve all favourites planets of this user
      favs = Favourites.objects.filter(ACCOUNT=self.request.user, RESOURCE_TYPE="PLANET")

      #empty list if no results
      if favs is None:
          return []
      
      #put retrieved items in list of dicts
      listFavs = []
      for fav in favs:
          listFavs.append({"name" : fav.NAME, "resource" : fav.RESOURCE_NAME, "type" : fav.RESOURCE_TYPE, "url" : fav.URL})
      
      return listFavs


  #add to favourites, return 0 if fail, 1 if success, return -1 if name is taken or resource has already been added
  def addFavourite(self, name, resourceName, resourceType, url):
      
      #Add data to Favourites table
      
      #If already present in favourites
      if Favourites.objects.filter(
              NAME=name.strip(), 
              ACCOUNT=self.request.user) or Favourites.objects.filter(
                  RESOURCE_NAME=resourceName.strip(), 
                  RESOURCE_TYPE=resourceType.strip(),
                  ACCOUNT=self.request.user
       ):
          return -1
      
      
      #If any error return 0
      try:
          newFav = Favourites(
              NAME=name.strip(), 
              RESOURCE_NAME=resourceName.strip(), 
              RESOURCE_TYPE=resourceType.strip(), 
              ACCOUNT=self.request.user, 
              URL=url.strip()
          )
          newFav.save()
      except:
          #On failure return 0
          return 0
      
      #On succesful add return 1
      return 1
  
    
  #add to favourites, return 0 if fail, 1 if success, return -1 if name is taken or resource has already been added
  def renameFavourite(self, new_name, name, resourceType, url):
      
      #Add data to Favourites table
      
      #If already present in favourites
      if Favourites.objects.filter(
              NAME=new_name.strip(),
              ACCOUNT=self.request.user):
          return -1
      
        
      #Update name
      #If any error return 0
      try:
          Favourites.objects.filter(NAME=name.strip(), 
          RESOURCE_TYPE=resourceType.strip(),
          URL=url.strip(),
          ACCOUNT=self.request.user
          ).update(NAME=new_name.strip())

      except:
          #On failure return 0
          return 0
      
      #On succesful add return 1
      return 1
  
  #delete favourite entry, return 0 if fail, 1 if success
  def deleteFavourite(self, name, fav_type, url):
      
      #Delete from Favourites table
      #If any error return 0
      try:
          delFav = Favourites.objects.filter(
              NAME=name.strip(), 
              RESOURCE_TYPE=fav_type.strip(), 
              URL=url.strip(), 
              ACCOUNT=self.request.user
          )
          delFav.delete()
      except:
          #On failure return 0
          return 0
      
      #On succesful delete return 1
      return 1
  
    
  #search favourites list
  def search(self, query):
      
      preparedQuery = re.sub(r"\s+", '', query.strip()).upper()
      
      ###RETRIEVE FAVOURITES AND MAKE UPPER
      favouriteList = self.getAllFavouritesList()
      
      favouriteResults = []
      
      #Find matches
      #Find position of query
      #Position not used due to inefficiency - reduce further ineficiency
      for i in favouriteList:
          preparedVal = re.sub(r"\s+", '', i["name"]).upper()
          pos = preparedVal.find(preparedQuery)
          if pos > -1:
              #add to reults if match
              favouriteResults.append(i)
    
      return favouriteResults
  
    
    
  #Check if resource is already in favourite, True if yes, False otherwise
  def is_favourite(self, resourceName):
      
      #Check if resource is present in favourites
      try:
          if Favourites.objects.filter(RESOURCE_NAME=resourceName.strip(), ACCOUNT=self.request.user).exists():
              return True
      except:
          return False
      
      return False
      

  #get favourites name of the resource, if not in favourites, return passed in name
  def favourite_name(self, resourceName):
      
      #if not in favourites, return original name
      if not self.is_favourite(resourceName):
          return resourceName
      
      #Get Favourite name
      else:
          #Retrieve record from DB
          fav = Favourites.objects.filter(RESOURCE_NAME=resourceName.strip(), ACCOUNT=self.request.user)
          #If more than one record (impossible), return the resource name passed to this function
          if (len(fav) != 1):
              return resourceName
          else:
              #Return the favourite name
              return str(fav.NAME)
              
              