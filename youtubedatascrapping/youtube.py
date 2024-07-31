import streamlit as st
from googleapiclient.discovery import build
import mysql.connector
import pandas as pd
import re
from datetime import datetime, timedelta

# Google API setup
api_service_name = "youtube"
api_version = "v3"
api_id = "AIzaSyAy02cRJCU3d9bttjN76E7lZ154FbPanLg"
youtube = build(api_service_name, api_version, developerKey=api_id)

def get_channel_info(ch_id):
    request = youtube.channels().list(
        id=ch_id,
        part='contentDetails, snippet, statistics, status'
    )
    response = request.execute()
    channel_information = {
        "playlist_id": response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
        "Channel_Id": response['items'][0]["id"],
        "channel_description": response['items'][0]['snippet']['description'],
        "channel_logo": response['items'][0]['snippet']['thumbnails']['default']['url'],
        "channel_title": response['items'][0]['snippet']['title'],
        "Subscriber_count": response['items'][0]['statistics']['subscriberCount'],
        "view_count": response['items'][0]['statistics']['viewCount'],
        "video_count": response['items'][0]['statistics']['videoCount'],
    }
    return channel_information

def get_playlist_details(ch_id):
    playlist_details = []
    next_page_token = None
    while True:
        request = youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=ch_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:
            playlist_info = {
                "playlist_title": item['snippet']['title'],
                "channel_title": item['snippet']['channelTitle'],
                "Channel_Id": item['snippet']['channelId'],
                "Playlist_Id": item['id'],
                "Video_Count": item['contentDetails']['itemCount']
            }
            playlist_details.append(playlist_info)
        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break
    return playlist_details

def get_video_id(playlist):
    video_id = []
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            playlistId=playlist,
            part='contentDetails, snippet,status',
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:
            video_id.append(item['contentDetails']['videoId'])
        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break
    return list(set(video_id))

def get_video_data(videoid):
    video_data = []
    for video_ids in videoid:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_ids
        )
        response = request.execute()
        videos_info = {
            "video_title": response['items'][0]['snippet']['title'],
            "comment_count": response['items'][0]['statistics'].get('commentCount'),
            "like_count": response['items'][0]['statistics'].get('likeCount'),
            "view_count": response['items'][0]['statistics'].get('viewCount'),
            "Published_Date": response['items'][0]['snippet']['publishedAt'],
            "Duration": response['items'][0]['contentDetails']['duration'],
            "licensed_content": response['items'][0]['contentDetails']['licensedContent'],
            "description": response['items'][0]['snippet'].get('description'),
            "Channel_Name": response['items'][0]['snippet']['channelTitle'],
            "Channel_Id": response['items'][0]['snippet']['channelId']
        }
        video_data.append(videos_info)
    return video_data

def get_comment_details(videoid):
    comment_data = []
    for video_ids in videoid:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_ids,
                maxResults=50
            )
            response = request.execute()
            comment_info = {
                "display_name": response['items'][0]['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                "Comment_Id": response['items'][0]['snippet']['topLevelComment']['id'],
                "Video_Id": response['items'][0]['snippet']['topLevelComment']['snippet']['videoId'],
                "comment": response['items'][0]['snippet']['topLevelComment']['snippet']['textDisplay']
            }
            comment_data.append(comment_info)
        except:
            pass
    return comment_data

def channel_table(channel_info):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Joshua@2020",
        database="youtube"
    )
    mycursor = mydb.cursor()
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS Channel (
            playlist_id VARCHAR(20), 
            Channel_Id varchar(100) PRIMARY KEY, 
            channel_description TEXT, 
            channel_logo TEXT, 
            channel_title TEXT, 
            Subscriber_count INTEGER, 
            view_count INTEGER, 
            video_count INTEGER
        )
    ''')
    columns = ', '.join(channel_info.keys())
    placeholders = ', '.join(['%s'] * len(channel_info))
    sql = 'INSERT IGNORE INTO Channel ({}) VALUES ({})'.format(columns, placeholders)
    try:
        mycursor.execute(sql, tuple(channel_info.values()))
        mydb.commit()
    except:
        pass
    mycursor.close()
    mydb.close()

def playlist_table(playlist_info):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Joshua@2020",
        database="youtube"
    )
    mycursor = mydb.cursor()
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS playlists (
            playlist_title varchar(100) PRIMARY KEY, 
            channel_title VARCHAR(100), 
            Channel_Id varchar(100), 
            Playlist_Id varchar(100), 
            Video_Count INTEGER
        )
    ''')
    for play in playlist_info:
        columns = ', '.join(play.keys())
        placeholders = ', '.join(['%s'] * len(play))
        sql = 'INSERT IGNORE INTO playlists ({}) VALUES ({})'.format(columns, placeholders)
        mycursor.execute(sql, tuple(play.values()))
        mydb.commit()
    mycursor.close()
    mydb.close()

def video_table(videodata):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Joshua@2020",
        database="youtube"
    )
    mycursor = mydb.cursor()
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS video (
            video_title varchar(100) PRIMARY KEY, 
            comment_count INTEGER, 
            like_count INTEGER, 
            view_count INTEGER, 
            Published_Date DATETIME, 
            Duration TIME, 
            licensed_content BOOLEAN, 
            description TEXT, 
            Channel_Name VARCHAR(100), 
            Channel_Id VARCHAR(100)
        )
    ''')
    for vid in videodata:
        vid = {k.lower(): v for k, v in vid.items()}
        if 'published_date' in vid:
            published_date_str = vid['published_date']
            published_date = datetime.strptime(published_date_str, '%Y-%m-%dT%H:%M:%SZ')
            vid['published_date'] = published_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            continue
        if 'duration' in vid:
            duration_str = vid['duration']
            match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration_str)
            hours = int(match.group(1)[:-1]) if match.group(1) else 0
            minutes = int(match.group(2)[:-1]) if match.group(2) else 0
            seconds = int(match.group(3)[:-1]) if match.group(3) else 0
            duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            vid['duration'] = str(duration)
        else:
            continue
        columns = ', '.join(vid.keys())
        placeholders = ', '.join(['%s'] * len(vid))
        sql = 'INSERT IGNORE INTO video ({}) VALUES ({})'.format(columns, placeholders)
        mycursor.execute(sql, tuple(vid.values()))
        mydb.commit()
    mycursor.close()
    mydb.close()

def comment_table(commentd):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Joshua@2020",
        database="youtube"
    )
    mycursor = mydb.cursor()
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS comment (
            display_name varchar(100), 
            Comment_Id varchar(100) PRIMARY KEY, 
            Video_Id varchar(100), 
            comment TEXT
        )
    ''')
    for comments in commentd:
        columns = ', '.join(comments.keys())
        placeholders = ', '.join(['%s'] * len(comments))
        sql = 'INSERT IGNORE INTO comment ({}) VALUES ({})'.format(columns, placeholders)
        mycursor.execute(sql, tuple(comments.values()))
        mydb.commit()
    mycursor.close()
    mydb.close()

def tables(channel_info, playlist_info, videodata, commentd):
    channel_table(channel_info)
    playlist_table(playlist_info)
    video_table(videodata)
    comment_table(commentd)
    return "Tables Created Successfully"

# Streamlit interface
st.title("YouTube Data Harvesting and Warehousing")
ch_id = st.text_input("Enter Channel ID")
if st.button("Extract Data"):
    channel_info = get_channel_info(ch_id)
    playlist = channel_info["playlist_id"]
    playlist_info = get_playlist_details(ch_id)
    videoid = get_video_id(playlist)
    videodata = get_video_data(videoid)
    commentd = get_comment_details(videoid)
    tables(channel_info, playlist_info, videodata, commentd)
    st.write("Data extraction and storage completed.")

option = st.selectbox(
    'Select the table to view',
    ('Channel', 'Playlists', 'Video', 'Comments')
)

if st.button("Retrieve Data"):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Joshua@2020",
        database="youtube"
    )
    mycursor = mydb.cursor()
    if option == 'Channel':
        mycursor.execute('SELECT * FROM Channel')
    elif option == 'Playlists':
        mycursor.execute('SELECT * FROM playlists')
    elif option == 'Video':
        mycursor.execute('SELECT * FROM video')
    elif option == 'Comments':
        mycursor.execute('SELECT * FROM comment')
    data = mycursor.fetchall()
    df = pd.DataFrame(data, columns=[desc[0] for desc in mycursor.description])
    st.write(df)
    mycursor.close()
    mydb.close()

# Additional functionality for specific queries
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Joshua@2020",
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

mycursor = mydb.cursor()
if question == "1. All the videos and the channel name":
    query1 = 'SELECT video_title, Channel_Name FROM video'
    mycursor.execute(query1)
    t1 = mycursor.fetchall()
    df = pd.DataFrame(t1, columns=["video title", "channel name"])
    st.write(df)
elif question == "2. Channels with most number of videos":
    query2 = 'SELECT channel_title, video_count FROM channel ORDER BY video_count DESC LIMIT 1'
    mycursor.execute(query2)
    t2 = mycursor.fetchall()
    df2 = pd.DataFrame(t2, columns=["channel name", "No of videos"])
    st.write(df2)
elif question == "3. 10 most viewed videos":
    query3 = 'SELECT video_title, view_count, Channel_Name FROM video ORDER BY view_count DESC LIMIT 10'
    mycursor.execute(query3)
    t3 = mycursor.fetchall()
    df3 = pd.DataFrame(t3, columns=["video title", "view count", "channel name"])
    st.write(df3)
elif question == "4. Comments in each video":
    query4 = 'SELECT video_title, comment_count, Channel_Name FROM video'
    mycursor.execute(query4)
    t4 = mycursor.fetchall()
    df4 = pd.DataFrame(t4, columns=["video title", "comment count", "channel name"])
    st.write(df4)
elif question == "5. Videos with highest likes":
    query5 = 'SELECT video_title, like_count, Channel_Name FROM video ORDER BY like_count DESC'
    mycursor.execute(query5)
    t5 = mycursor.fetchall()
    df5 = pd.DataFrame(t5, columns=["video title", "like count", "channel name"])
    st.write(df5)
elif question == "6. Likes of all videos":
    query6 = 'SELECT video_title, like_count, Channel_Name FROM video'
    mycursor.execute(query6)
    t6 = mycursor.fetchall()
    df6 = pd.DataFrame(t6, columns=["video title", "like count", "channel name"])
    st.write(df6)
elif question == "7. Views of each channel":
    query7 = 'SELECT Channel_Name, SUM(view_count) FROM video GROUP BY Channel_Name'
    mycursor.execute(query7)
    t7 = mycursor.fetchall()
    df7 = pd.DataFrame(t7, columns=["channel name", "total views"])
    st.write(df7)
elif question == "8. Videos published in the year of 2022":
    query8 = 'SELECT Channel_Name, video_title, Published_Date FROM video WHERE YEAR(Published_Date) = 2022'
    mycursor.execute(query8)
    t8 = mycursor.fetchall()
    df8 = pd.DataFrame(t8, columns=["channel name", "video title", "published date"])
    st.write(df8)
elif question == "9. Average duration of all videos in each channel":
    query9 = 'SELECT Channel_Name, SEC_TO_TIME(AVG(TIME_TO_SEC(Duration))) AS Average_Duration FROM video GROUP BY Channel_Name'
    mycursor.execute(query9)
    t9 = mycursor.fetchall()
    df9 = pd.DataFrame(t9, columns=["channel name", "average duration"])
    st.write(df9)
elif question == "10. Videos with highest number of comments":
    query10 = 'SELECT video_title, comment_count, Channel_Name FROM video ORDER BY comment_count DESC'
    mycursor.execute(query10)
    t10 = mycursor.fetchall()
    df10 = pd.DataFrame(t10, columns=["video title", "comment count", "channel name"])
    st.write(df10)

mycursor.close()
mydb.close()