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
        with open('in.csv','r',errors='ignore') as csv_file:
          csv_reader = csv.reader(csv_file)
            
          for line in csv_reader:
            # city = line[0]
            lat = line[1]
            lng = line[2]
            search_params = {
                'key' : current_app.config['YOUTUBE_API_KEY'],
                'q' : request.form.get('query'),
                'part' : 'snippet',
                'maxResults' : 9 ,
                'type' : 'video',
                # 'channelType' : 'show',
                # 'relevanceLanguage':'te',
                'location':f'{lat},{lng}',
                'locationRadius': '1000km'
            }
            print("Test start")
            print(lat)
            print(lng)
            print("Test end")
            r = requests.get(search_url, params=search_params)
            print("This is the response")
            print(r.json())
            results = r.json()['items']
            print(results)
            # video_ids = []
            for result in results:
                video_ids.append(result['id']['videoId'])

        if request.form.get('submit') == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'id' : ','.join(video_ids),
            'part' : 'snippet,contentDetails',
            # 'regionCode':'IN',
            'maxResults' : 9,
            # 'h1':'te'
        }

        r = requests.get(video_url, params=video_params)
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
