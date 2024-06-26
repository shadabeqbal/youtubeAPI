from service.service import *
from service.processing import *

def scheduled_update():
    try:
        # Fetch all unique channels from the VideoDetails table
        channels = db.session.query(VideoDetails.channel_id, VideoDetails.channel_name).distinct().all()
        channel_ids = [channel[0] for channel in channels]
        # Update video data
        update_video_details(channel_ids)
        
        for channel in channels:
            # Re-fetch updated video data
            updated_video_data = VideoDetails.query.filter_by(channel_id=channel).all()

            # Recalculate insights
            extract_top_keywords_and_store(updated_video_data)
            analyze_engagement_metrics(updated_video_data)

    except Exception as e:
        print(f"Error in scheduled update: {e}")