from flask import Blueprint, jsonify
from service.service import *
from service.processing import *
from service.updater import *
from flask import request

api = Blueprint('api', __name__)

@api.route('/health', methods=['GET'])
def health():
    """
    Health Check
    ---
    responses:
      200:
        description: Health Check
    """
    return f"Health: OK"

@api.route('/populate_videos', methods=['POST'])
def service():
    """
Load youtube video details of multiple channels
---
parameters:
  - name: body
    in: body
    description: JSON object containing a list of channel IDs
    required: true
    schema:
      type: object
      properties:
        channel_id:
          type: array
          items:
            type: string
responses:
  200:
    description: Populate the MYSQL database with the channel videos info
    schema:
      type: object
      properties:
        message:
          type: string
"""

    #channel_id = ['UCly5GYgMHb58yjrzLqNbURA']
    if request.is_json:
        channel_id = request.json.get('channel_id', [])
    else:
        channel_id = request.form.getlist('channel_id')
    
    if not channel_id:
        return jsonify({"error": "Channel ID list is empty"}), 400
    
    result = populate_youtube_videos(channel_id)
    return jsonify({"message": result})

@api.route('/analyze_for_channel/<channel_id>', methods=['POST'])
def populate_analyze_metrics(channel_id):
    """
    Populate into DB all analysis metrics by channel ID
    ---
    parameters:
      - name: channel_id
        in: path
        type: string
        required: true
        description: The channel ID
    responses:
      200:
        description: A list of analysis metrics
        schema:
          type: array
          items:
            type: object
            properties:
              channel_id:
                type: string
                description: The ID of the channel
              channel_name:
                type: string
                description: The name of the channel
              total_like:
                type: integer
                description: The total number of likes
              total_comments:
                type: integer
                description: The total number of comments
              average_likes:
                type: number
                format: float
                description: The average number of likes
              average_comments:
                type: number
                format: float
                description: The average number of comments
              engagement_rate:
                type: number
                format: float
                description: The engagement rate
      404:
        description: Channel not found
      500:
        description: Internal Server Error
    """
    response = analyze_for_channel(channel_id)
    return response

@api.route('/videos/<channel_id>', methods=['GET'])
def videos(channel_id):
  """
    Get videos by channel ID
    ---
    parameters:
      - name: channel_id
        in: path
        type: string
        required: true
        description: The channel ID
    responses:
      200:
        description: A list of videos
        schema:
          type: array
          items:
            type: object
            properties:
              video_id:
                type: string
              title:
                type: string
              description:
                type: string
              view_count:
                type: integer
              like_count:
                type: integer
              comment_count:
                type: integer
              publication_date:
                type: string
              channel_id:
                type: string
              channel_name:
                type: string
      404:
        description: Channel not found
      500:
        description: Internal Server Error
    """
  return get_videos_by_channel(channel_id)

@api.route('/get_analyze_metrics/<channel_id>', methods=['GET'])
def get_analyze_metrics_details(channel_id):
    """
    Get analysis metrics by channel ID
    ---
    parameters:
      - name: channel_id
        in: path
        type: string
        required: true
        description: The channel ID
    responses:
      200:
        description: A list of analysis metrics
        schema:
          type: array
          items:
            type: object
            properties:
              channel_id:
                type: string
                description: The ID of the channel
              channel_name:
                type: string
                description: The name of the channel
              total_like:
                type: integer
                description: The total number of likes
              total_comments:
                type: integer
                description: The total number of comments
              average_likes:
                type: number
                format: float
                description: The average number of likes
              average_comments:
                type: number
                format: float
                description: The average number of comments
              engagement_rate:
                type: number
                format: float
                description: The engagement rate
      404:
        description: Channel not found
      500:
        description: Internal Server Error
    """
    return get_analyze_metrics(channel_id)
  
@api.route('/get_top_keywords/<channel_id>', methods=['GET'])
def get_keywords(channel_id):
    """
    Get Top keywords by channel ID
    ---
    parameters:
      - name: channel_id
        in: path
        type: string
        required: true
        description: The channel ID
    responses:
      200:
        description: Top keywords for the specified channel
        schema:
          type: object
          properties:
            channel_id:
              type: string
              description: The ID of the channel
            channel_name:
              type: string
              description: The name of the channel
            top_keywords:
              type: array
              items:
                type: string
              description: List of top keywords associated with the channel
      404:
        description: No top keywords found for the specified channel ID
      500:
        description: Internal Server Error
    """
    return get_top_keywords(channel_id)