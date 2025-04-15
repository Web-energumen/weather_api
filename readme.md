# Weather API

## Project Overview

Python sample solution for the [Weather API](https://roadmap.sh/projects/weather-api-wrapper-service) challenge from [roadmap.sh](https://roadmap.sh/).

This project is a simple Django REST Framework-based Weather API that retrieves weather data from a third-party provider (Visual Crossing Weather API) using location and an optional date range. It implements Redis caching to reduce external requests and includes rate limiting to prevent abuse.

## Features

* Fetch Weather Data: Retrieve weather data by location (city name, ZIP code, or coordinates) with optional start_date and end_date filters.
* Caching: Uses Redis to cache weather data for 6 hours, reducing external API calls and improving response times.
* Rate Limit: Limits the number of requests to the API to prevent abuse. For anonymous users - 50 requests per hour, for authorised users - 100 requests per hour.
* Handles cases such as invalid locations, third-party API failures, and internal server errors.

## Technologies Used

* Django: Python web framework.
* Django REST Framework: Toolkit for building Web APIs.
* Requests: Python library for making HTTP requests to the third-party weather API.
* Visual Crossing Weather API: External service providing weather data.

## API Usage

### Base URL
The API is hosted locally at:
`http://localhost:8000/api/weather/`

### Request Format
#### Example Request
```
curl "http://localhost:8000/api/weather/Kharkiv/2025-04-15/"
```

### Query Parameters
* `location`(required): address, ZIP code or latitude, longitude location for which to retrieve weather data.
* `date1`(optional): the start date of receiving weather data in yyyy-MM-dd format. If this value is omitted, the current date is used by default.
* `date2`(optional): the final date for receiving weather data in the format yyyy-MM-dd. This value can only be used if date1 is set.

### Response
The API returns weather data in JSON format.

### Example Response:
``` json
{
"queryCost": 1,
    "latitude": 50.0042,
    "longitude": 36.2358,
    "resolvedAddress": "Харків, Україна",
    "address": "kharkiv",
    "timezone": "Europe/Kiev",
    "tzoffset": 3.0,
    "description": "Similar temperatures continuing with no rain expected.",
    "days": [
        {
            "datetime": "2025-04-15",
            "datetimeEpoch": 1744664400,
            "tempmax": 18.8,
            "tempmin": 6.0,
            ...
            "stations": [
                "UUOB"
            ],
            "source": "comb",
            "hours": [
                {
                    "datetime": "00:00:00",
                    "datetimeEpoch": 1744664400,
                    "temp": 11.0,
                    ...
                    "stations": [
                        "UUOB"
                    ],
                    "source": "obs"
                },
                ...
            ]
        },
        ...
    ]
    "alerts": [],
    "stations": {
        "UUOB": {
            "distance": 73835.0,
            "latitude": 50.63,
            "longitude": 36.58,
            "useCount": 0,
            "id": "UUOB",
            "name": "UUOB",
            "quality": 50,
            "contribution": 0.0
        }
    },
    "currentConditions": {
    "datetime": "14:00:00",
    "datetimeEpoch": 1744714800,
    "temp": 18.0,
    "feelslike": 18.0,
    ...
    }
}
```

## Installation

### Prerequisites
* Python 3.10+
* Redis: Ensure that Redis is installed and running.
* Visual Crossing Weather API Key: Sign up and obtain an API key from Visual Crossing.

### Steps
1. **Clone the Repository**:
    ``` bash
      git clone https://github.com/Web-energumen/weather_api.git
      cd weather_api
    ```

2. **Set Up Virtual Environment**:
    ```bash
      python3 -m venv venv
      source venv/bin/activate
    ```

3. **Install Dependencies**:
    ```bash
      pip install -r requirements.txt
    ```

4. **Configure Environment Variables**:  Create a .env file in the root directory and add:
    ```
      VISUAL_CROSSING_API_KEY=your_api_key
    ```

5. **Apply Migrations**:
    ```bash
      python3 manage.py migrate
    ```

6. **Run Redis**: Make sure Redis is running locally. If Redis isn't installed, you can install it on Ubuntu using:
    ```bash
      sudo apt update
      sudo apt install redis-server
    ```

    Start Redis and check:

    ```bash
      sudo systemctl start redis
      redis-cli ping
    ```

7. **Run the Django server**:
    ```bash
      python3 manage.py runserver
    ```

8. Test the API: Use curl or a browser to access the API:
    ```bash
      curl "http://localhost:8000/api/weather/Kharkiv/2025-04-15/"
    ```

## Rate Limiting
API limits the number of requests for anonymous users - 50 requests per hour, for authorised users - 100 requests per hour. If this limit is exceeded, the API will return a `429 Too Many Requests` response.

## Caching
Redis is used to cache weather data for 6 hours. If a request is made for the same location and date during this time, the cached data will be returned instead of a new API call to an external service.

## Error Handling
* **Invalid Location**: When the API cannot find the specified city, we return an error with a 404 code and a message.
* **Service Unavailable**: When there is a problem connecting to a third-party API, return an error with code 503 (Service Unavailable) and a description of the problem.
* **Rate Limit Exceeded**: If the user exceeds the request limit, the API will return a 429 status and an over limit message.
* **Bad Request**: If the location parameter is not passed, the API will return an error with the code 400 and the corresponding message.
