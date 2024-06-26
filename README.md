# YouTube Channel Video Analysis API

This API provides endpoints to interact with YouTube channel data, including loading video details, analyzing metrics, and retrieving information for specific channels.

## Table of Contents
- [Endpoints](#endpoints)
  - [Health Check](#health-check)
  - [Populate YouTube Videos](#populate-youtube-videos)
  - [Populate Analysis Metrics by Channel ID](#populate-analysis-metrics-by-channel-id)
  - [Get Videos by Channel ID](#get-videos-by-channel-id)
  - [Get Analysis Metrics by Channel ID](#get-analysis-metrics-by-channel-id)
  - [Get Top Keywords by Channel ID](#get-top-keywords-by-channel-id)
- [Setup](#setup)
- [Usage](#usage)

## Setup

1. Clone the repository:
    ```sh
    git clone <repository_url>
    ```

2. Navigate to the project directory:
    ```sh
    cd <project_directory>
    ```

3. Install Dependencies:
    ```sh
    pip install -r requirements.txt

    MYSQL Server 5.7.43
    ```

4. Change config details in `config.properties` file:
    ```ini
    [youtube]
    API_KEY = <your_api_key>

    [database]
    DB_USERNAME = root
    DB_PASSWORD = root
    DB_HOST = localhost
    DB_PORT = 3306
    DB_NAME = youtube
    ```

## Usage

you can create virtual environment to run it locally, which will not impract your global settings (optional)
```sh
python -m venv <env-name>

<env-name>/Scripts/activate (to activate virtualenv)

deactivate (to deactivate virtual env)
```

For running the app, simply run:
```sh
python main.py

open http://localhost:5000/apidocs
```

## Endpoints

#### `GET /health`

**Description:**
Checks the health of the service.

**Responses:**
- `200 OK`: Returns a message indicating that the service is healthy.

"Health: OK"

#### `POST /populate_videos`

**Description:**
Loads YouTube video details of multiple channels and populates the MySQL database with the channel videos info.

**Responses:**
- `200 OK`: 
{
  "message": "YouTube videos populated successfully"
}

#### `POST /analyze_for_channel/<channel_id>`

**Description:**
Populates the database with all analysis metrics by the provided channel ID.

**Parameters**
channel_id (string ): The YouTube channel ID.

**Responses:**
- `200 OK`: 
[
  {
    "channel_id": "Uidjsi238u4kdf",
    "channel_name": "Sample Channel",
    "total_like": 1000,
    "total_comments": 200,
    "average_likes": 50.0,
    "average_comments": 10.0,
    "engagement_rate": 0.05
  }
]

#### `GET /videos/<channel_id>`

**Description:**
Retrieves a list of videos by the provided channel ID.

**Parameters**
channel_id (string, in path): The YouTube channel ID.

**Responses:**
- `200 OK`: 
[
  {
    "video_id": "xyz123",
    "title": "Sample Video",
    "description": "This is a sample video description.",
    "view_count": 1000,
    "like_count": 100,
    "comment_count": 20,
    "publication_date": "2023-01-01 12:00:00",
    "channel_id": "UCly5GYgMHb58yjrzLqNbURA",
    "channel_name": "Sample Channel"
  }
]

#### `GET /get_analyze_metrics/<channel_id>`

**Description:**
Retrieves analysis metrics by the provided channel ID.

**Parameters**
channel_id (string, in path): The YouTube channel ID.

**Responses:**
- `200 OK`: 
[
  {
    "channel_id": "Uidjsi238u4kdf",
    "channel_name": "Sample Channel",
    "total_like": 1000,
    "total_comments": 200,
    "average_likes": 50.0,
    "average_comments": 10.0,
    "engagement_rate": 0.05
  }
]

#### `GET /get_top_keywords/<channel_id>`

**Description:**
Retrieves top keywords by the provided channel ID.

**Parameters**
channel_id (string, in path): The YouTube channel ID.

**Responses:**
- `200 OK`: 
{
    "channel_id": "Uidjsi238u4kdf",
    "channel_name": "Sample Channel",
    "top_keywords": {
        "action": 6,
        "agent": 9,
        "channel": 6,
        "gameplay": 8,
        "gaming": 8
    }
}





