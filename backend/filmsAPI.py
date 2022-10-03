#To facilitate search
import re
import datetime

#Imorting parent class
from . StarWarsAPI import StarWarsAPI

#Importing favourites
from . userFavourites import userFavourites


class filmsAPI(StarWarsAPI):
    
  # Get Base API URL
  def __init__(self, request):
    super().__init__()
    self.url = self.getURLEndpoint()
    self.request = request
    
 
    
    
  # get data of all Movies to expose API
  def getAllMoviesData(self):
      
      # Get all planet data using parent class method with Movies url
      allMoviesData = super().getResourceData(self.url)
      
      # If API URL Could not be resolved, return error in dict
      if len(allMoviesData)!=0 and "error" in allMoviesData[0]:
          return [{"error" : "Resource API endpoint could not be resolved"}]
      
      #Validate Data  
      if not self.validateData(allMoviesData):
          return [{"error" : "Retrieved Data is Malformed"}]
      
      #Filter the data to return only necessary values
      allMoviesData = self.filterData(allMoviesData)     
      
      return allMoviesData
   
    
   
  # get data of single Movies based on URL
  def getSingleMovieData(self, movieURL):
      
      # Get all planet data using parent class method with Movies url
      movieData = super().getSingleResourceData(movieURL)
      
      # If API URL Could not be resolved, return error in dict
      if len(movieData)==0:
          return {"error" : "No Data Retrieved"}
      elif "error" in movieData[0]:
          return {"error" : "Error retrieving data"}
      
      #Validate Data  
      if not self.validateData(movieData):
          return {"error" : "Retrieved Data is Malformed"}
      
      #Resolve URLs and populate data
      movieRetrieved = self.populateSingleMovieData(movieData[0])
      
      #return dict of movie info
      return movieRetrieved



  #Search for Movie Names
  def search(self, query):
      
      #Add search query to url as described in documentation to url
      url = self.url
      preparedQuery = re.sub(r"\s+", '%20', query.strip())
      urlQuery = url+ "?search=" + preparedQuery
      
      #get results by calling API
      searchResults = super().getResourceData(urlQuery)
      
      # If API URL Could not be resolved, return error in dict
      if len(searchResults)!=0 and "error" in searchResults[0]:
          return [{"error" : "Resource API endpoint could not be resolved"}]
      
      # filter data
      filteredResults = self.filterData(searchResults, True) 
      
      return filteredResults
  
    

  # Filter the retrived data so the exposed API only contains the required data
  #Empty list signifies no search results
  def filterData(self, data, validated=True):  
      
      filteredData = []
      
      #Get all favourite movies
      favObj = userFavourites(self.request)
      favourites = favObj.getFavouriteFilmsList()
      
      #If data has not been validated before
      if (not validated) and (not self.validateData(data)):
              return [{"error" : "Retrieved Data is Malformed"}]          
      
      # Iterate through List
      for i in data:            
          
          is_favourite = False
          favName = i["title"]
          
          #check if in favourites
          #replace name with favourites name if so
          for fav in favourites:
              if i["title"].strip() == fav["resource"].strip():
                  favName = fav["name"]
                  is_favourite = True
                  break
          
          # Add only required field as per instructions
          filteredData.append(
              {
                   "title" : favName, 
                   "release_date" : datetime.datetime.strptime(
                       i["release_date"], '%Y-%m-%d').strftime("%B %d, %Y"), 
                   "created" : datetime.datetime.strptime(
                       i["created"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%I:%M %p on %B %d, %Y"),
                   "updated" : datetime.datetime.strptime(
                       i["edited"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%I:%M %p on %B %d, %Y"), 
                   "url" : i["url"], 
                   "is_favourite" : is_favourite
               }
          )
          
      return filteredData
      

  # Gets API endpoint to get Movies information
  def getURLEndpoint(self):
      
      allResources = super().getAllResourceURLs()
      
      # if 'films' is in all resources obtained from parent class, return the planet url, else, empty string
      if "films" in allResources:
          return allResources["films"]
      else:
          return ""  
      
    
  #Retrieve details from links in data
  def populateSingleMovieData(self, data):
      
      #Make sure required data is present
      if (
              not("species" in data)) or (
                  not("starships" in data)) or (
                      not("vehicles" in data)) or (
                          not("characters" in data)) or (
                              not("planets" in data)
         ):
          return [{"error":"Incorrect Data Received"}]
      
      species = []
      
      #Populate species info
      for i in data["species"]:
          tmp = super().getSingleResourceData(i)
          if (len(tmp)!=0) and ("name" in tmp[0]):
              species.append(tmp[0]["name"])
              
      starships = []
      
      #Populate starships info
      for i in data["starships"]:
          tmp = super().getSingleResourceData(i)
          if (len(tmp)!=0) and ("name" in tmp[0]):
              starships.append(tmp[0]["name"])
              
      vehicles = []
      
      #Populate vehicles info
      for i in data["vehicles"]:
          tmp = super().getSingleResourceData(i)
          if (len(tmp)!=0) and ("name" in tmp[0]):
              vehicles.append(tmp[0]["name"])
              
      characters = []
      
      #Populate characters info
      for i in data["characters"]:
          tmp = super().getSingleResourceData(i)
          if (len(tmp)!=0) and ("name" in tmp[0]):
              characters.append(tmp[0]["name"])

      planets = []

      #Populate planets info
      for i in data["planets"]:
          tmp = super().getSingleResourceData(i)
          if (len(tmp)!=0) and ("name" in tmp[0]):
              planets.append(tmp[0]["name"])                

      #Replave URLs with names and titles of resources
      data["species"] = species
      data["starships"] = starships
      data["vehicles"] = vehicles
      data["characters"] = characters
      data["planets"] = planets
      data["release_date"] = datetime.datetime.strptime(
          data["release_date"], '%Y-%m-%d').strftime("%B %d, %Y")
      data["created"] = datetime.datetime.strptime(
          data["created"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%I:%M %p on %B %d, %Y")
      data["edited"] = datetime.datetime.strptime(
          data["edited"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%I:%M %p on %B %d, %Y")
      
      #return dictionary of planet data
      return data
    
      
        
  # Check if all variables are present of the correct type and format if applicable
  #Empty list signifies no search results
  def validateData(self, data):
      
      # Validate Data type in dictionary
      attributes = {
          "title":" ",
          "episode_id": -1,
          "opening_crawl":" ",
          "director":" ",
          "producer":" ",
          "release_date":" ",
          "species":[],
          "starships":[],
          "vehicles":[],
          "characters":[],
          "planets":[],
          "url":" ",
          "created":" ",
          "edited":" "
      }
      
      # Check if data is present and of valid type and form when applicable
      baseURL = super().getURL().strip()
      
      for i in data:
          for j in attributes:
              if j not in i:
                  #error
                  return False
              elif type(attributes[j]) is not type(i[j]):
                  #error
                  return False
              #Validate url by checking if parent/Base API url is present in it
              elif (j == "url") and (not(i[j].strip()).startswith(baseURL)):
                  return False
          
      return True
  