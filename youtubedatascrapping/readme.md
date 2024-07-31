# YouTube Data Harvesting and Warehousing

YouTube Data Harvesting and Warehousing is a project designed to provide users with the ability to access and analyze data from numerous YouTube channels. This project utilizes SQL, MongoDB, and Streamlit to develop a user-friendly application for retrieving, saving, and querying YouTube channel and video data.

## Tools and Libraries Used

### Streamlit
Streamlit is used to create an interactive user interface for the application. It enables users to perform data retrieval and analysis operations through a web-based application.

### Python
Python is the primary programming language used for the development of this application. It is utilized for data retrieval, processing, analysis, and visualization.

### Google API Client
The `googleapiclient` library is used to interact with YouTube's Data API v3. This library facilitates the retrieval of essential information such as channel details, video specifics, and comments from YouTube.

### MySQL
MySQL is an open-source relational database management system used to store and manage structured data. It supports various data types and advanced SQL capabilities for efficient data management and querying.

## Features

1. **Retrieval of Channel and Video Data**: Access detailed information about YouTube channels and videos using the YouTube API.
2. **Data Storage**: Store the retrieved data in a MongoDB database for scalable data management.
3. **Data Migration**: Migrate data from MongoDB to a MySQL database for efficient querying and analysis.
4. **Data Retrieval and Analysis**: Use various query options to search and retrieve data from the MySQL database.

## Libraries Required

1. `googleapiclient.discovery`
2. `streamlit`
3. `re` (Regular Expression)
4. `datetime`, `timedelta`
5. `pandas`

## Ethical Considerations

When scraping YouTube data, it is essential to adhere to ethical practices:
- **Respect YouTube's Terms of Service**: Ensure that the scraping activities comply with YouTube's terms and conditions.
- **Obtain Authorization**: Use appropriate API keys and authorization methods.
- **Data Protection**: Handle collected data responsibly, ensuring privacy and confidentiality.
- **Impact on Platform**: Consider the potential impact on the platform and its community, aiming for fair and sustainable data extraction.

## Installation and Setup

1. **Install Dependencies**: Ensure that you have all the required libraries installed. You can install them using pip:
    ```bash
    pip install google-api-python-client pandas streamlit mysql-connector-python
    ```

2. **API Key**: Replace the `api_id` in the code with your YouTube Data API v3 key.

3. **Database Setup**:
    - **MySQL**: Set up MySQL and create the necessary databases and tables as described in the code.

4. **Run the Application**:
    - Start the Streamlit application by executing the following command:
      ```bash
      streamlit run your_script.py
      ```

## Usage

1. **Enter the Channel ID**: Input the desired YouTube channel ID in the Streamlit UI.
2. **Migrate Data to SQL**: Click the "Migrate to SQL" button to transfer data from MongoDB to the MySQL database.
3. **Select Queries**: Use the provided options to query and view data from the MySQL database.

## Code

The main Python script for this project is designed to interact with the YouTube API, retrieve data, and manage it using SQL and MongoDB. Below is an outline of the key functions and operations:

```python
# Importing necessary libraries
from googleapiclient.discovery import build
import mysql.connector
import pandas as pd
import re
from datetime import datetime, timedelta
import streamlit as st

# Initialize API connection
api_service_name = "youtube"
api_version = "v3"
api_id = "YOUR_API_KEY"
youtube = build(api_service_name, api_version, developerKey=api_id)

# Define functions for data retrieval and processing

def get_channel_info(ch_id):
    # Function to get channel information
    ...

def get_playlist_details(ch_id):
    # Function to get playlist details
    ...

def get_video_id(playlist):
    # Function to get video IDs from a playlist
    ...

def get_video_data(videoid):
    # Function to get video data
    ...

def get_comment_details(videoid):
    # Function to get comment details
    ...

def channel_table():
    # Function to create and populate the Channel table in MySQL
    ...

def playlist_table():
    # Function to create and populate the Playlists table in MySQL
    ...

def video_table():
    # Function to create and populate the Video table in MySQL
    ...

def comment_table():
    # Function to create and populate the Comment table in MySQL
    ...

def tables():
    # Function to create all tables in MySQL
    ...

# Streamlit UI
st.title(":red[YOUTUBE DATA HARVESTING AND WAREHOUSING]")
st.header("Skill Take Away")
st.caption("Python Scripting")
st.caption("Data Collection")
st.caption("MongoDB")
st.caption("API Integration")
st.caption("Data Management using MongoDB and SQL")

ch_id = st.text_input("Enter the channel ID")

if st.button("Migrate to SQL"):
    result = tables()
    st.success(result)

show_table = st.radio("SELECT THE TABLE FOR VIEW", ("CHANNELS", "PLAYLISTS", "VIDEOS", "COMMENTS"))
if show_table == "CHANNELS":
    show_channels_table()
elif show_table == "PLAYLISTS":
    show_playlists_table()
elif show_table == "VIDEOS":
    show_videos_table()
elif show_table == "COMMENTS":
    show_comment_table()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="youtube"
)

question = st.selectbox("Select your question", (
    "1. All the videos and the channel name",
    "2. Channels with most number of videos",
    "3. 10 most viewed videos",
    "4. Comments in each video",
    "5. Videos with highest likes",
    "6. Likes of all videos",
    "7. Views of each channel",
    "8. Videos published in the year of 2022",
    "9. Average duration of all videos in each channel",
    "10. Videos with highest number of comments"
))

# Query execution based on selected question
...

