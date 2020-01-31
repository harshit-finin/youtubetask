import requests
from isodate import parse_duration
import csv
from flask import Blueprint, render_template, current_app, request, redirect

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():

    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []
    video_ids = []

    if request.method == 'POST':
    
            # To search we have to provide the following parameters according to YOUTUBE DATA API
            search_params = {
                'key' : current_app.config['YOUTUBE_API_KEY'],
                'q' : request.form.get('query'),
                'part' : 'snippet',
                'maxResults' : 9 ,
                'type' : 'video',
                # 'channelType' : 'show',
                # 'relevanceLanguage':'te',
                'location':'27.0238,74.2179',
                'locationRadius': '1000km'
            }
            # Getting search results
            r = requests.get(search_url, params=search_params)

            results = r.json()['items']
            # video_ids = []
            # storing search videos Id
            for result in results:
                video_ids.append(result['id']['videoId'])

    if request.form.get('submit') == 'lucky':
        return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

    # fetching videos information to fetch it we have to provide the following parameters
    video_params = {
        'key' : current_app.config['YOUTUBE_API_KEY'],
        'id' : ','.join(video_ids),
        'part' : 'snippet,contentDetails',
        # 'regionCode':'IN',
        'maxResults' : 9,
        # 'h1':'te'
    }
    # Response according to params
    r = requests.get(video_url, params=video_params)
    # storing the video info. 
    results = r.json()['items']
    for result in results:
        video_data = {
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
            'thumbnail' : result['snippet']['thumbnails']['high']['url'],
            'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
            'title' : result['snippet']['title'],
        }
        videos.append(video_data)

    return render_template('index.html', videos=videos)