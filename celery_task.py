from celery import Celery
import requests
import time

# Define the URL and headers
url = 'https://ranking.glassdollar.com/graphql'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Content-Type': 'application/json',
}

app = Celery('celery_task',backend="rpc://" , broker='pyamqp://')

@app.task
def getCorporateByID(corporateID, counter):
    print("TaskQueue Count : " + str(counter))
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
            return current_corporate
        else:
            print("Unexpected response format. 'data' key not found.")
