import requests
import json

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

# Make the POST request with the GraphQL query
response1 = requests.post(url, headers=headers, json=getCorporateCities_query)
response2 = requests.post(url, headers=headers, json=getCorporateIndustries_query)

corporate_cities, corporate_industries = [], []
# Check if the request was successful
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

#print (corporate_cities_string)
#print (corporate_industries_string)

# We define page variable that changes too get all the data avaliable
page = 1
hasNextPage = True
#all_corporates_without_startup_partners = [] not necessary
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
            #all_corporates_without_startup_partners.extend(current_corporates)
            #print(current_corporates)
            page += 1
        else:
            print("Unexpected response format. 'data' key not found.")
    else : 
        print(f"Failed to retrieve data. Status code: {response3.status_code}")

all_corporates = []

# Since corporate info we got from the pages did not have the start-up partners info,
# we will get the corporateID's from earlier and use it to find the corporate information 
# for each corporate one by one. 

counter=0

for corporateID in all_corporate_ids:
    counter += 1
    print(counter) # counter just to see the process

    getCorporateByID_query = {
    "operationName": "GetCorporate",
    "variables": {},
    "query": "query GetCorporate {  corporate(id : \""+ corporateID +"\")   {    id     name    description    logo_url    hq_city    hq_country    website_url    linkedin_url    twitter_url    startup_partners_count    startup_partners    {      company_name      logo      city      website      country      theme_gd    }    startup_themes  }}"
    }
    response4 = requests.post(url, headers=headers, json=getCorporateByID_query)
    if response4.status_code == 200:
        data = response4.json()

        if 'data' in data:
            # Extract 'getCorporateCities' data
            current_corporate = data['data'].get('corporate', {})
            all_corporates.append(current_corporate)
        else:
            print("Unexpected response format. 'data' key not found.")

# We save the info to the all_corporates.json file
with open('all_corporates.json', 'w') as json_file:
    json.dump(all_corporates, json_file, indent=2)

print("All corporates data saved to all_corporates.json.")

