from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
LASTFM_BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

def get_track_tags(artist, track):
    params = {
        'method': 'track.getTopTags',
        'artist': artist,
        'track': track,
        'api_key': LASTFM_API_KEY,
        'format': 'json'
    }
    response = requests.get(LASTFM_BASE_URL, params=params)
    data = response.json()
    tags = []
    if 'toptags' in data:
        tags = [tag['name'].lower() for tag in data['toptags']['tag'][:10]]
    return tags

def get_similar_tracks(artist, track, limit=20):
    params = {
        'method': 'track.getSimilar',
        'artist': artist,
        'track': track,
        'api_key': LASTFM_API_KEY,
        'format': 'json',
        'limit': limit
    }
    response = requests.get(LASTFM_BASE_URL, params=params)
    data = response.json()
    tracks = []
    if 'similartracks' in data:
        tracks = data['similartracks']['track']
    return tracks

def find_common_tags(tags1, tags2):
    set1 = set(tags1)
    set2 = set(tags2)
    common = list(set1.intersection(set2))
    unique1 = list(set1 - set2)
    unique2 = list(set2 - set1)
    return common, unique1, unique2

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_track')
def search_track():
    query = request.args.get('q', '')
    params = {
        'method': 'track.search',
        'track': query,
        'api_key': LASTFM_API_KEY,
        'format': 'json',
        'limit': 5
    }
    response = requests.get(LASTFM_BASE_URL, params=params)
    data = response.json()
    tracks = []
    if 'results' in data:
        tracks = data['results']['trackmatches']['track']
    return jsonify(tracks)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    song1 = data.get('song1')
    song2 = data.get('song2')
    playlist_size = int(data.get('size', 10))

    tags1 = get_track_tags(song1['artist'], song1['track'])
    tags2 = get_track_tags(song2['artist'], song2['track'])

    common_tags, unique1, unique2 = find_common_tags(tags1, tags2)

    similar1 = get_similar_tracks(song1['artist'], song1['track'], limit=50)
    similar2 = get_similar_tracks(song2['artist'], song2['track'], limit=50)

    def score_track(track, common_tags):
        return track.get('match', 0)

    combined = {t['name'] + t['artist']['name']: t for t in similar1}
    for t in similar2:
        key = t['name'] + t['artist']['name']
        if key in combined:
            combined[key]['match'] = float(combined[key].get('match', 0)) + float(t.get('match', 0))
        else:
            combined[key] = t

    playlist = sorted(combined.values(), key=lambda x: float(x.get('match', 0)), reverse=True)[:playlist_size]

    result = []
    for track in playlist:
        artist_name = track['artist']['name'] if isinstance(track['artist'], dict) else track['artist']
        track_name = track['name']
        result.append({
            'track': track_name,
            'artist': artist_name,
            'spotify_url': f"https://open.spotify.com/search/{requests.utils.quote(track_name + ' ' + artist_name)}",
            'apple_music_url': f"https://music.apple.com/search?term={requests.utils.quote(track_name + ' ' + artist_name)}",
            'youtube_music_url': f"https://music.youtube.com/search?q={requests.utils.quote(track_name + ' ' + artist_name)}"
        })

    return jsonify({
        'playlist': result,
        'tags': {
            'common': common_tags,
            'song1_unique': unique1[:5],
            'song2_unique': unique2[:5]
        }
    })

if __name__ == '__main__':
    app.run(debug=True)