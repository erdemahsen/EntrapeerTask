## How to run the program ?

1 - Clone this repository to local with following command.
```
git clone https://github.com/erdemahsen/EntrapeerTask.git
```
2 - Go to the EntrapeerTask folder that is cloned.
```
cd EntrapeerTask
```
3 - Build docker image with following command.
```
docker build -t entrapeer .
```
4 - Compose the docker containers with the following command.
```
docker compose up -d
``` 
5 - Now open 3 terminals and at each one of them use the following command :
```
docker exec -it server bash
```
```
docker exec -it server bash
```
```
docker exec -it server bash
```
6 - In the first terminal type the following command to run Celery task :
```
celery -A celery_task worker --loglevel=INFO
```
7 - In the second terminal type the following command to run the FastAPI, make it avaliable for access :
```
uvicorn entrapeer:app --host 0.0.0.0 --port 8000 --reload
```
8 - Now open your browser and navigate to the following link.
```
http://localhost:8000/corporates
```
Allow some time for the corporates to load. Requests will be displayed in the Celery terminal.
At the end of this process on the browser you will see a list of corporates with all of the fetched information, and also this information will be saved in json format to "all_corporates.json" file.

9 - Now go to the third terminal and enter the following code to do the Machine Learning task.
```
python3 groupCompanies.py
```
Code above will use the data from "all_corporates.json", and classify the corporates into 10 groups. Result will be saved to "grouped_companies.xlxs"

## Some information about the program

- After 2th step you can use the following command to remove precalculated "all_corporates.json" and "grouped_companies.xlxs".
Since all of the files are copied to docker, we may want to calculate the results in docker using the instructions above.
```
rm grouped_companies.xlxs
```
```
rm all_corporates.json
```
- If you have done the instructions above correctly you will have "all_corporates.json" and "grouped_companies.xlxs" files created in the docker.
- You can use "ls" command to see the files in the directory. 
- You can check all_corporates.json for all of the corporates data, and check grouped_companies.xlxs to see the corporates in groups.
- "groupCompanies.py" takes first 10 corporates and creates groups for each of them. After that for each corporate I checked the closeness to these 10 corporates, and put the corporate to the group that has the highest similarity. I used vector-embeddings on the description of each corporate. So they are grouped according to their description similarity.
- According to task at the 8th step I was suppose to add a comeback later message however I did not add it, "http://localhost:8000/corporates" does not show anything till it loads fully.
- If you have any questions please let me know.

# Ömer Erdem Ahsen
