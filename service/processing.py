
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk
from datetime import datetime
from flask import jsonify
import json

nltk.download('punkt')
nltk.download('stopwords')

from database.video_details import VideoDetails
from database.trends import Trends
from database.top_keywords import TopKeywords
from database.analyze_metrics import AnalyzeMetrics

from utils.conn import db

def analyze_for_channel(channelId):
    video_data = VideoDetails.query.filter_by(channel_id=channelId).all()
    
    view_count_trends = calculate_view_count_trends(video_data)
    top_keywords = extract_top_keywords_and_store(video_data)
    engagement_metrics = analyze_engagement_metrics(video_data)
    print(view_count_trends)
    return view_count_trends

def calculate_view_count_trends(video_data):
    
    channel_id = video_data[0].channel_id
    channel_name = video_data[0].channel_name
    
    dates = [(datetime.strptime(video.publication_date, '%Y-%m-%dT%H:%M:%SZ').day,
              datetime.strptime(video.publication_date, '%Y-%m-%dT%H:%M:%SZ').month,
              datetime.strptime(video.publication_date, '%Y-%m-%dT%H:%M:%SZ').year) for video in video_data]
    
    view_counts_per_date = {}
    for day, month, year in set(dates):
        view_counts_per_date[(day, month, year)] = sum([video.view_count for video in video_data if (datetime.strptime(video.publication_date, '%Y-%m-%dT%H:%M:%SZ').day,
                                                                                                               datetime.strptime(video.publication_date, '%Y-%m-%dT%H:%M:%SZ').month,
                                                                                                               datetime.strptime(video.publication_date, '%Y-%m-%dT%H:%M:%SZ').year) == (day, month, year)])
 
    for (day, month, year), views in view_counts_per_date.items():
        existing_trend = Trends.query.filter_by(channel_id=channel_id, day=day, month=month, year=year).first()
        if existing_trend:
            existing_trend.views = views
        else:
            trend = Trends(channel_id=channel_id, channel_name=channel_name, views=views, day=day, month=month, year=year)
            db.session.add(trend)
    
    db.session.commit()

    return {"message": "Channel view trends calculated and stored successfully"}
    
    

def extract_top_keywords_and_store(video_data):
    channel_id = video_data[0].channel_id
    channel_name = video_data[0].channel_name
    
    all_titles = ' '.join([video.title for video in video_data])
    all_descriptions = ' '.join([video.description for video in video_data])
    all_text = all_titles + ' ' + all_descriptions

    tokens = word_tokenize(all_text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    word_freq = Counter(filtered_tokens)
    top_keywords = word_freq.most_common(10)  # Get the top 10 keywords

    # Convert top_keywords to a string
    top_keywords_str = json.dumps(dict(top_keywords))

    # Store the top keywords in the database, avoiding duplicates
    existing_entry = TopKeywords.query.filter_by(channel_id=channel_id, channel_name=channel_name).first()
    if existing_entry:
        existing_entry.top_keywords = top_keywords_str
        db.session.commit()
    else:
        keyword_entry = TopKeywords(channel_id=channel_id, channel_name=channel_name, top_keywords=top_keywords_str)
        db.session.add(keyword_entry)
        db.session.commit()

    return {"message": "Top keywords extracted and stored successfully"}

def analyze_engagement_metrics(video_data):
    channel_id = video_data[0].channel_id
    channel_name = video_data[0].channel_name
    total_likes = sum([video.like_count for video in video_data])
    total_comments = sum([video.comment_count for video in video_data])
    average_likes = total_likes / len(video_data)
    average_comments = total_comments / len(video_data)
    engagement_rate = average_likes / average_comments if average_comments != 0 else 0

    # Store the engagement metrics in the database, avoiding duplicates
    existing_entry = AnalyzeMetrics.query.filter_by(channel_id=channel_id, channel_name=channel_name).first()
    if existing_entry:
        existing_entry.total_like = total_likes
        existing_entry.total_comments = total_comments
        existing_entry.average_likes = average_likes
        existing_entry.average_comments = average_comments
        existing_entry.engagement_rate = engagement_rate
    else:
        metrics_entry = AnalyzeMetrics(
            channel_id=channel_id,
            channel_name=channel_name,
            total_like=total_likes,
            total_comments=total_comments,
            average_likes=average_likes,
            average_comments=average_comments,
            engagement_rate=engagement_rate
        )
        db.session.add(metrics_entry)

    db.session.commit()

    return {
        'total_likes': total_likes,
        'total_comments': total_comments,
        'average_likes': average_likes,
        'average_comments': average_comments,
        'engagement_rate': engagement_rate
    }

def get_top_keywords(channel_id):
    try:
        top_keywords = TopKeywords.query.filter_by(channel_id=channel_id).all()
        
        if not top_keywords:
            return jsonify({"message": f"No top keywords metrics found for channel ID {channel_id}"}), 404
        
        
        keyword_entry = {
            'channel_id': top_keywords[0].channel_id,
            'channel_name': top_keywords[0].channel_name,
            'top_keywords': json.loads(top_keywords[0].top_keywords)
        }

        return jsonify(keyword_entry), 200

    except Exception as e:
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500
        
        
def get_analyze_metrics(channel_id):
    try:
        # Fetch all analysis metrics for the given channel_id
        metrics_data = AnalyzeMetrics.query.filter_by(channel_id=channel_id).all()

        if not metrics_data:
            return jsonify({"message": f"No analysis metrics found for channel ID {channel_id}"}), 404

        # Prepare the metrics data to be returned as JSON
        metrics_list = []
        for metric in metrics_data:
            metric_entry = {
                'channel_id': metric.channel_id,
                'channel_name': metric.channel_name,
                'total_like': metric.total_like,
                'total_comments': metric.total_comments,
                'average_likes': metric.average_likes,
                'average_comments': metric.average_comments,
                'engagement_rate': metric.engagement_rate
            }
            metrics_list.append(metric_entry)

        return jsonify(metrics_list), 200

    except Exception as e:
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500