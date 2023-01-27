# Flask project

1. Install docker with docker and docker compose. Follow this link instructions https://docs.docker.com/compose/install/.

2. Clone this repository.

3. Go to this repository directory and build the image:


```
docker compose build
```


4. Run the services (backend and database):


```
docker compose up
```

5. Populate the db with fake data:


```
docker compose exec backend python3 create_fake_db.py
```

6. Go to http://localhost:5000/institutions and try the Rest API's
