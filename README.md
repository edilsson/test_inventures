# URL Shortener Project

### Developed by Edilsson Bravo (@edilsson)

### Deployed version - http://146.190.173.125/

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
We're currently using SQLite for this project. There's only one table handling the complete solution.
```
class ShortenedURL(Base):
    """Model class for shortened URLs."""

    __tablename__ = "shortened_urls"

    id = Column(Integer, primary_key=True)
    original_url = Column(String, index=True)
    alias = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    expires_at = Column(DateTime)
    clicks = Column(Integer, default=0)
```
We are using indexes for `original_url` and `alias` in order to make faster searches for those cases. Also, `alias` has to be an unique value in order to handle each URL correctly.

In terms of scalability, it could happen that the table grows exponentially. So, there's the chance we may need to change the database engine to something more robust (PostgreSQL, or even BigQuery in GCP). Also, in order to have more traceability, this table cannot help us, so there's a need to add more relations in the model.

## API Endpoints

### `/shorten` - Generate Shorten URL

This endpoints checks if the `url` is valid, generates an `alias` (if the user didn't send a custom one), and inserts it on the database with an expiration of 3 days.

If the `custom_alias` sent by the user already exists on a different **non-expired** shortened `url`, then the service will return a `400` error.

Request:
```
{
  "url": "string",
  "custom_alias": "string" (Optional)
}
```

Response:
```
{
  "original_url": "string",
  "alias": "string",
  "created_at": "2025-03-31T02:00:53.565Z",
  "expires_at": "2025-03-31T02:00:53.565Z",
  "clicks": 0
}
```

### `/stats` - Get URL Stats

Shows the full list of shortened URLs and the click stats. Also, brings the dates of creation and expiration.

There are some filters that we are not using in frontend, mainly related to shortness of time, but they are available in some form from the backend.

Request:
```
(query params, all fields Optional)
{
  "status": ["ACTIVE", "INACTIVE"],
  "sort_by": ["clicks", "original_url", "alias"],
  "page": int (default = 1),
  "size": int (default = 100),
}
```

Response:
```
[
  {
    "original_url": "string",
    "alias": "string",
    "created_at": "2025-03-31T02:04:40.905Z",
    "expires_at": "2025-03-31T02:04:40.905Z",
    "clicks": 0
  }
]
```

### `/{alias}` - Redirect to URL
Gets the `alias`, checks if exists on the database, then, if it's not expired, adds one extra `click` to the counter, to finally make a redirect to the `original_url`.

Response:
```
302
```

## Assumptions and TODOs

- There's a complete lack of testing in both backend and frontend.
- There are some implementations that could be improved (the ones that appear with a `TODO` on the code.)
- For the sake of time, we are not ordering the Stats results on the frontend.
- After creating a new shortened URL, we're missing the table reload to show the new URL.
- UI/UX could be easily improved. Shortness of time deeply impacted on this area.