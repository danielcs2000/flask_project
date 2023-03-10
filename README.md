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

6. Go to http://localhost:5000/ and try the Rest API's (Swagger)

# Postman Collection (LOCAL)

Go to the link to see the Postman collection for a local environment 

https://elements.getpostman.com/redirect?entityId=25222599-44bf8e77-1492-42ac-82c2-67e659ea2308&entityType=collection

![image](https://user-images.githubusercontent.com/34191864/215221076-83af675b-eea3-4480-a467-463a968dd109.png)


# Swagger Screenshot

![image](https://user-images.githubusercontent.com/34191864/215286381-1342816f-a7f4-4f1c-ad68-5b2907e30dc6.png)


# Future steps

- Handle errors
- Custom error messages
- Unit tests

