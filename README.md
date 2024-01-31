## How to run the program ?

1 - Clone this repository with following command :
```
git clone https://github.com/erdemahsen/EntrapeerTask.git
```
2 - Go to the folder where Dockerfile is and build image with following command :
```
docker build -t entrapeer .
```
3 - Compose the docker with the following command : 
```
docker compose up -d
``` 
4 - Now open 3 terminals and at each one of them use the following command :
```
docker exec -it server bash
```
5 - In the first terminal type the following command to create Celery task :
```
celery -A celery_task worker --loglevel=INFO
```
6 - In the second terminal type the following command to run the fastAPI, make it avaliable for access :
```
uvicorn entrapeer:app --host 0.0.0.0 --port 8000 --reload
```
7 - Now open your browser and enter to the following link, it will take some time do not close the window and at the end you should see all of the corporates on a list, it is saved in all_corporates.json.
At the time you should see celery window processing the corporates
```
http://localhost:8000/corporates
```
8 - Now go to the 3rd terminal and enter the following code to do the ML part.
```
python3 groupCompanies.py
```
It is done you can check all_corporates.json for all of the corporates, and check grouped_companies.xlxs to see the grouped version of them
This corporates are grouped with ...