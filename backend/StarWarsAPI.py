# To read config file
from pathlib import Path
import os
import configparser

# convert json response to dictionary
import json

import requests

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class StarWarsAPI:
    
  # Get Base API URL
  def __init__(self):
    self.baseURL = self.getBaseURL()
    
    
    
    
  # get URLs for all top level resources in API
  def getAllResourceURLs(self):
      
      url = self.baseURL
      resultURLs = {}
      
      if url == "":
          return {"error" : "Error Reading config file. Base API URL could not be resolved."}
      
      header = {
        "Content-Type":"application/json"
      }
      
      # Make get request to API and convert json response to dictionary
      # return json objects in dictionary on HTTP Status Code 200
      # return error in dictionary if request fails
      resultURLs = self.requestToSwAPI(url, header)
      
      return resultURLs




  # get all data of resource to expose API
  def getResourceData(self, url):
      
      allResourceData = []
      
      # If API URL Could not be resolved, return error in dict
      if url == "":
          return [{"error" : "Resource API endpoint could not be resolved"}]
      
      header = {
        "Content-Type":"application/json"
      }
      
      # Make get request to API and convert json response to dictionary
      # return json objects in dictionary on HTTP Status Code 200
      # return error in dictionary if fail
      resultData = self.requestToSwAPI(url, header)
      if "error" in resultData:
          return [resultData]
      
      # If results are in the response, assign it to the return value list
      if "results" in resultData:
          allResourceData = resultData["results"]
      else:
          return [{"error" : "Unexpected data in results"}]
      
      # If a next page is mentioned and present in the json response, print other responses
      # If key parameters are present in the response, proceed to extract rest of the data
      # else, return empty dictionary
      if (
              ("next" in resultData) and 
              (resultData["next"] is not None) and 
              ("count" in resultData)
      ):
          
          # Initialize counter to number of items already retrived
          # Keep requesting successive items until we reach count sent in the request
          counter = len(resultData["results"])
          
          #While counter is less than total count returned from request
          while (counter < resultData["count"]):
              
              # make HTTPS call again for next elements
              resultData = self.requestToSwAPI(resultData["next"], header)
              if "error" in resultData:
                  return [resultData]
              
              #Ensure Data is valid
              #Append all new data to list if valid
              if "results" in resultData:
                  allResourceData.extend(resultData["results"])
              else:
                  return [{"error" : "Unexpected data in results"}]
              
              # Increase counter by number of elements added
              counter += len(resultData["results"])
              
      
      # return json objects in dictionary on HTTP Status Code 200
      # skip values that give error codes
      # return error in list if there is an error
      return allResourceData



  # get single resource data of for page data
  def getSingleResourceData(self, url):
      
      # If API URL Could not be resolved, return error in dict
      if url == "":
          return [{"error" : "Resource API endpoint could not be resolved"}]
      
      header = {
        "Content-Type":"application/json"
      }
      
      # Make get request to API and convert json response to dictionary
      # return json objects in dictionary on HTTP Status Code 200
      # return error in dictionary if fail
      resultData = self.requestToSwAPI(url, header)
      if "error" in resultData:
          return [resultData]

      # return json objects in dictionary on HTTP Status Code 200
      # return error in list if there is an error
      return [resultData]



  # Extract Base API URL from config file
  def getBaseURL(self):
      
    # Read config file
    keys = ["BASE_URL"]
    url = {}
    
    try:
        config = configparser.ConfigParser()
        config.read(os.path.join(BASE_DIR, 'config/config.ini'))
        
        try:       
            for key in keys:
                url[key] = config.get("URL", key)
        except configparser.NoOptionError:
            print(f"Cannot find {key} in config File read, please make sure config file is set up correctly")
            return ""
    except:
        print("Config File read faced an error, please make sure config file is in the path")
        return ""
    
    # If URL is not found, return empty string
    if 'BASE_URL' in url:
        return url['BASE_URL']
    else:
        print("\nCan NOT find Base URL in config file, please ensure config file is set up correctly.")
        
    return ""




  # Make get request to API and convert json response to dictionary
  # return json objects in dictionary on HTTP Status Code 200
  # return error key in dictionary if request fails
  def requestToSwAPI(self, url, header):
        
    resultData = {}
    try:
        result = requests.get(url,headers=header)
        if result.status_code == 200:
            resultData = json.loads(result.content)
        else:
            resultData["error"] = "HTTPS request failed: " + str(result.status_code) + " Error"
    except:
        resultData["error"] = "Error while making HTTPS Request"  
           
    return resultData



  def getURL(self):
    return self.baseURL