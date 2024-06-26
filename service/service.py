
from googleapiclient.discovery import build
from database.video_details import VideoDetails
from utils.configReader import ConfigReader
from utils.conn import db
from flask import jsonify
config_obj = ConfigReader()
config = config_obj.get_youtube_config()


def get_youtube_service():
    return build(config['YOUTUBE_API_SERVICE_NAME'], config['YOUTUBE_API_VERSION'], developerKey=config['API_KEY'])

def fetch_video_ids(channel_id):
    try:
        youtube = get_youtube_service()
        next_page_token = None
        videoIds = []
        while True:
            tempIds = []
            request = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            
            
            for item in response['items']:
                if item['id']['kind'] == 'youtube#video':
                    video_id = item['id']['videoId']
                    tempIds.append(video_id)
            
            
            videoIds.extend(tempIds)
            next_page_token = response.get('nextPageToken')
            
            if not next_page_token:
                break
            
        return videoIds
    except Exception as e:
        return "Error! Fetching video Ids failed: " + str(e) 

def fetch_video_list(videoIds):
    try:
        videos = []
        youtube = get_youtube_service()
        for i in range(0, len(videoIds), 50):
            chunk = videoIds[i:i+50]
            video_details_response = youtube.videos().list(
                part='snippet,statistics',
                id=','.join(chunk)
            ).execute()
            
            for each_video in video_details_response['items']:
                video_data = VideoDetails(
                    video_id=each_video['id'],
                    title=each_video['snippet']['title'],
                    description=each_video['snippet']['description'],
                    view_count=int(each_video['statistics']['viewCount']),
                    like_count=int(each_video['statistics']['likeCount']),
                    comment_count=int(each_video['statistics']['commentCount']),
                    publication_date=each_video['snippet']['publishedAt'],
                    channel_id=each_video['snippet']['channelId'],
                    channel_name=each_video['snippet']['channelTitle']
                )
                videos.append(video_data)
        
        return videos
    except Exception as e:
        return "Error! Fetching video details failed: " + str(e) 

def populate_youtube_videos(channelIds):
    try:
        for channel in channelIds:
            videoIds = fetch_video_ids(channel)
            video_data = fetch_video_list(videoIds)
            all_video_data = []
            # Prepare video data for bulk insertion
            for data in video_data:
                existing_video = VideoDetails.query.filter_by(video_id=data.video_id, channel_id=channel).first()
                if existing_video is None:
                    video_entry = {
                        'video_id': data.video_id,
                        'title': data.title,
                        'description': data.description,
                        'view_count': data.view_count,
                        'like_count': data.like_count,
                        'comment_count': data.comment_count,
                        'publication_date': data.publication_date,
                        'channel_id': data.channel_id,
                        'channel_name': data.channel_name
                    }
                    all_video_data.append(video_entry)
            
            db.session.bulk_insert_mappings(VideoDetails, all_video_data)
            db.session.commit()
            
            return "data loaded successfully"
    except Exception as e:
        return "Error! Loading into database failed: " + str(e)

def update_video_details(channelIds):
    try:
        for channel in channelIds:
            videoIds = fetch_video_ids(channel)
            video_data = fetch_video_list(videoIds)

            for data in video_data:
                existing_video = VideoDetails.query.filter_by(video_id=data.video_id, channel_id=channel).first()
                
                if existing_video:
                    # Update the existing video record with new data
                    existing_video.title = data.title
                    existing_video.description = data.description
                    existing_video.view_count = data.view_count
                    existing_video.like_count = data.like_count
                    existing_video.comment_count = data.comment_count
                    existing_video.publication_date = data.publication_date
                    existing_video.channel_name = data.channel_name
                else:
                    # Insert new video record if it does not exist
                    new_video = VideoDetails(
                        video_id=data.video_id,
                        title=data.title,
                        description=data.description,
                        view_count=data.view_count,
                        like_count=data.like_count,
                        comment_count=data.comment_count,
                        publication_date=data.publication_date,
                        channel_id=data.channel_id,
                        channel_name=data.channel_name
                    )
                    db.session.add(new_video)
            
            db.session.commit()
            
            return "Database updated successfully"
    except Exception as e:
        return "Error! Updating database failed: " + str(e)

def get_videos_by_channel(channel_id):
    try:
        # Fetch all videos for the given channel_id
        video_data = VideoDetails.query.filter_by(channel_id=channel_id).all()

        # Prepare the video data to be returned as JSON
        video_list = []
        for video in video_data:
            video_entry = {
                'video_id': video.video_id,
                'title': video.title,
                'description': video.description,
                'view_count': video.view_count,
                'like_count': video.like_count,
                'comment_count': video.comment_count,
                'publication_date': video.publication_date,
                'channel_id': video.channel_id,
                'channel_name': video.channel_name
            }
            video_list.append(video_entry)

        # Return the video data as a JSON object
        return jsonify(video_list)
    except Exception as e:
        return jsonify({'error fetching video details for a channel': str(e)})
