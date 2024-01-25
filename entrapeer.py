import requests
import json
from celery_task import getCorporateByID
from celery import group
from fastapi import FastAPI, BackgroundTasks
from typing import List
from contextlib import asynccontextmanager

 # Define the URL and headers
url = 'https://ranking.glassdollar.com/graphql'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Content-Type': 'application/json',
}

# Define the GraphQL query for GetCorporateCities
getCorporateCities_query = {
    "operationName": "GetCorporateCities",
    "variables": {},
    "query": "query GetCorporateCities {getCorporateCities}"
}

getCorporateIndustries_query = {
    "operationName": "GetCorporateIndustries",
    "variables": {},
    "query": "query GetCorporateIndustries {getCorporateIndustries}"
}
app = FastAPI()



@asynccontextmanager
async def fetch_corporates(app):
    # Make the POST request with the GraphQL query
    all_corporates = []
    try :
        print("Starting the crawling process...")
        response1 = requests.post(url, headers=headers, json=getCorporateCities_query)
        response2 = requests.post(url, headers=headers, json=getCorporateIndustries_query)

        corporate_cities, corporate_industries = [], []
        if response1.status_code == 200:
            data = response1.json()
            if 'data' in data:
                # Extract 'getCorporateCities' data
                corporate_cities = data['data'].get('getCorporateCities', [])
                print("Corporate Cities:", corporate_cities)
            else:
                print("Unexpected response format. 'data' key not found.")
        else:
            print(f"Failed to retrieve data. Status code: {response1.status_code}")

        if response2.status_code == 200:
            data = response2.json()
            if 'data' in data:
                # Extract 'getCorporateCities' data
                corporate_industries = data['data'].get('getCorporateIndustries', [])
                print("Corporate Industries:", corporate_industries)
            else:
                print("Unexpected response format. 'data' key not found.")
        #Algorithm to make the string of cities
        corporate_cities_string = "["
        for city in corporate_cities:
            if city is not None:
                corporate_cities_string += "\"" +city + "\", "
        if(corporate_cities_string[-2:] == ", "):
            corporate_cities_string = corporate_cities_string[:-2]
        corporate_cities_string += "]"

        #Algorithm to make the string of industries
        corporate_industries_string = "["
        for industry in corporate_industries:
            if industry is not None:
                corporate_industries_string += "\"" +industry + "\", "
        if(corporate_industries_string[-2:] == ", "):
            corporate_industries_string = corporate_industries_string[:-2]
        corporate_industries_string += "]"

        # We define page variable that changes too get all the data avaliable
        page = 1
        hasNextPage = True
        all_corporate_ids = []

        # We run over all pages and at each page we acquire multiple corporates each time
        # Since this query gets "hq_city" and "industry" as search filter we have gotten these info earlier
        while hasNextPage:
            getAllCorporates_query = {
            "operationName": "GetAllCorporates",
            "variables": {},
            "query": "query GetAllCorporates {corporates(page:"+ str(page)+", sortBy: \"revenue\", filters: {hq_city: "+corporate_cities_string+", industry: "+corporate_industries_string+"}) {rows {id name description logo_url website_url linkedin_url twitter_url industry hq_city hq_country startup_friendly_badge startup_partners_count}}}"
            }
            response3 = requests.post(url, headers=headers, json=getAllCorporates_query)
            if response3.status_code == 200:
                data = response3.json()
                if 'data' in data:
                    # Extract 'getCorporateCities' data
                    current_corporates = data['data'].get('corporates', {}).get('rows', [])
                    hasNextPage = len(current_corporates) > 0
                    for corporate in current_corporates:
                        if corporate['id'] not in all_corporate_ids:
                            all_corporate_ids.append(corporate['id'])
                    #print(current_corporates)
                    page += 1
                else:
                    print("Unexpected response format. 'data' key not found.")
            else : 
                print(f"Failed to retrieve data. Status code: {response3.status_code}")

        # Since corporate info we got from the pages did not have the start-up partners info,
        # we will get the corporateID's from earlier and use it to find the corporate information 
        # for each corporate one by one. 
        # This process is done in parallel using celery.

        all_corporates = []
        counter=0
        tasks = [getCorporateByID.s(corporateID, counter) for counter, corporateID in enumerate(all_corporate_ids, start=1)]

        async_result = group(*tasks).apply_async()

        # Retrieve results from the group
        results = async_result.get()

        # Process the results, this is not the most optimized way since it saves the results in a the all_corporates list
        for result in results:
            if result:
                all_corporates.append(result)
        print("Done crawling.")
        yield all_corporates
    finally:
        yield



#app = FastAPI(lifespan=lifespan)

@app.get("/corporates")
async def return_corporates():
    # Check if the crawling task is completed
    try: 

        async with fetch_corporates(app) as all_corporates:
            if len(all_corporates) == 847:
                # If task is ready, return the corporates list
                print("Data is ready.")
                writeToFile(all_corporates)
                return all_corporates
            else:
                # If task is not ready, return a message indicating the data is not yet available
                print("Data is not yet available. Please try again later.")
                return {"message": "Data is not yet available. Please try again later." + str(len(all_corporates))}
    except Exception as e:
        print("Error occured while fetching the corporates.")
        print(e)
        return all_corporates
        return {"message": "Error occured while fetching the corporates."}


def writeToFile(all_corporates):
    # We save the info to the all_corporates.json file
    with open('all_corporates.json', 'w') as json_file:
        json.dump(all_corporates, json_file, indent=2)
    print("All corporates data saved to all_corporates.json.")

print("All corporates data saved to all_corporates.json.")

