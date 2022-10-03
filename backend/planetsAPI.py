#To validate URLs
import re
import datetime

#Imorting parent class
from . StarWarsAPI import StarWarsAPI

#Importing favourites
from . userFavourites import userFavourites


class planetsAPI(StarWarsAPI):
    
  # Get Base API URL
  def __init__(self, request):
    super().__init__()
    self.url = self.getURLEndpoint()
    self.request = request
    
    
    
  # get data of all planets to expose API
  def getAllPlanetsData(self):
      
      # Get all planet data using parent class method with planets url
      allPlanetsData = super().getResourceData(self.url)
      
      # If API URL Could not be resolved, return error in dict
      if len(allPlanetsData) != 0 and "error" in allPlanetsData[0]:
          return [{"error" : "Resource API endpoint could not be resolved"}]
      
      #Validate Data  
      if not self.validateData(allPlanetsData):
          return [{"error" : "Retrieved Data is Malformed"}]
      
      #Filter the data to return only necessary values
      allPlanetsData = self.filterData(allPlanetsData)     
      
      return allPlanetsData


  # get data of single planets based on URL
  def getSinglePlanetData(self, planetURL):
      
      # Get all data of planet using parent class method with the planet url
      planetData = super().getSingleResourceData(planetURL)
      
      # If API URL Could not be resolved, return error in dict
      if len(planetData) == 0:
          return {"error" : "No data retrieved"}
      elif "error" in planetData[0]:
          return {"error" : "Issues retrieving data"}
      
      #Validate Data  
      if not self.validateData(planetData):
          return {"error" : "Retrieved Data is Malformed"} 
      
      #Resolve URLs and populate data
      planetRetrieved = self.populateSinglePlanetData(planetData[0])
      
      #return dict of planet info
      return planetRetrieved
  
    

  #Search for Planet Names
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
    
      
    
  # Gets API endpoint to get Planets information
  def getURLEndpoint(self):
      
      allResources = super().getAllResourceURLs()
      
      # if planets is in all resources obtained from parent class, return the planet url, else, empty string
      if "planets" in allResources:
          return allResources["planets"]
      else:
          return ""        
      



  # Filter the retrived data so the exposed API only contains the required data
  #Empty list signifies no search results
  def filterData(self, data, validated=True):  
      
      filteredData = []
      
      favObj = userFavourites(self.request)
      favourites = favObj.getFavouritePlanetsList()
      
      #If data has not been validated before
      if (not validated) and (not self.validateData(data)):
              return [{"error" : "Retrieved Data is Malformed"}]          
      
      # Iterate through List
      for i in data:            
          
          is_favourite = False
          favName = i["name"]
          
          #check if in favourites
          #replace name with favourites name if so
          for fav in favourites:
              if i["name"].strip() == fav["resource"].strip():
                  favName = fav["name"]
                  is_favourite = True
                  break
          
          # Add only required field as per instructions
          filteredData.append(
              {
                   "name" : favName, 
                   "created" : datetime.datetime.strptime(
                       i["created"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%I:%M %p on %B %d, %Y"),
                   "updated" : datetime.datetime.strptime(
                       i["edited"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%I:%M %p on %B %d, %Y"),
                   "url" : i["url"], 
                   "is_favourite" : is_favourite
               }
          )
          
      return filteredData
  
  
  
  #Retrieve details from links in data
  def populateSinglePlanetData(self, data):
      
      #
      if not("residents" in data) or not("films" in data):
          return [{"error":"Incorrect Data Received"}]
      
      residents = []
      
      #Populate Residents info
      for i in data["residents"]:
          resident = super().getSingleResourceData(i)
          if (len(resident)!=0) and ("name" in resident[0]):
              residents.append(resident[0]["name"])
              
      films = []
      
      #Populate Residents info
      for i in data["films"]:
          film = super().getSingleResourceData(i)
          if (len(film)!=0) and ("title" in film[0]):
              films.append(film[0]["title"])
              
      #Replave URLs with names and titles of resources
      data["residents"] = residents
      data["films"] = films
      data["created"] = datetime.datetime.strptime(
          data["created"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%I:%M %p on %B %d, %Y")
      data["edited"] = datetime.datetime.strptime(
          data["edited"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%I:%M %p on %B %d, %Y")
      
      #return dictionary of planet data
      return data
      
        
              
  # Check if all variables are present of the correct type and format if applicable
  #intentionally ignored empty list to accomodate search results
  def validateData(self, data):
      
      # Validate Data type in dictionary
      attributes = {
          "name":" ",
          "diameter":" ",
          "rotation_period":" ",
          "orbital_period":" ",
          "gravity":" ",
          "population":" ",
          "terrain":" ",
          "surface_water":" ",
          "residents":[],
          "films":[],
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
              elif (j == "url") and (not (i[j].strip()).startswith(baseURL)):
                  return False     
          
      return True