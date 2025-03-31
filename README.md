# URL Shortener Project

### Developed by Edilsson Bravo (@edilsson)

## Summary
Project developed for the recruitment process carried out by Inventures for March 2025.
A simple URL shortener, with click tracking, link expiration and a visualization web platform.

## Local setup
### Backend (FastAPI)
It's required to be on the root folder. It's also recommended to use a virtualenv.
```
pip install -r back_inventures/requirements.txt
uvicorn back_inventures.shortener:api
```

### Frontend (ReactJS)
You have to be inside `front_inventures` folder
```
npm config set legacy-peer-deps true
npm install
npm start 
```

## Setup with Docker (Production)
From the root folder, execute the following commands:
```
docker build -t back_inventures .
docker build -t front_inventures front_inventures/.
docker run --detach -p 8000:8000 back_inventures
docker run --detach -p 80:80 front_inventures
```
Now the frontend will be running from on the port 80.

TODO: Use `docker-compose`.

## Data model
There's only one table handling the complete solution.

```

```