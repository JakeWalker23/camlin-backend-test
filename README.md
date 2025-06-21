# Camlin Backend Engineer Test

Hello. Thank you for the opportunity to apply for this role at Camlin Group.




Please read on for full instructions to build and run the API. For example API usuage, please see the Postman collections [here](.postman/CamlinGroup.postman_collection.json).


### 1. Secrets

Create a .env file in the root of the repository. 


### 2. Generate JWT for HTTP requests

The JWT provides Authentication and Authorisation for the API.

Generate your JWT using this python script
```
python3 generate_token.py
```

Example headeer usage with HTTP client :

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NTA1MjI2OTh9.DODmqJ5o3-PfdNMWnKeEE6Yfl6ebzXghjuGKtwt4Q8o
```


### 3. Build & run using Docker

Build the application using docker:
```
docker build -t camlin-backend .
```


Run the application on port 8000:
```
docker run -p 8000:8000 camlin-backend
```



### 4. Use a HTTP client to communicate with the API

Recommended usage is Postman, as collections can be imported. But other methods could be Curl or httpie.

To import into Postman:
1. Open Postman
2. Click "Import"
3. Select "File"
4. Upload the `CamlinGroup.postman_collection.json` file


