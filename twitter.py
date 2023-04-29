import tweepy
import requests
import json 
import random
import time
import os


# API twitter credentiales
all_keys = open('twitter.txt', 'r').read().splitlines()
api_key = all_keys[0]
api_key_Secret = all_keys[1]
access_token = all_keys[2]
access_token_secret = all_keys[3]

# auth with API twitter
auth = tweepy.OAuth1UserHandler(api_key, api_key_Secret)
auth.set_access_token(access_token, access_token_secret)

#obj API twitter 
api = tweepy.API(auth)

#Acces token Deezer
deezer_access_token = open('access_token.txt', 'r').read().splitlines()
deezer_token = deezer_access_token[0]

#user id de deezer 
user_id = 729578273

def get_user_songs():
    url = f'https://api.deezer.com/user/{user_id}/tracks'
    headers = {'Authorization' : 'Bearer ' + deezer_token}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    songs = []

    for song in data['data']:
        songs.append({
            'id':song['id'],
            'title':song['title'],
            'artist':song['artist']['name'],
            'link': song['link'],
            'cover': song['album']['cover_xl']
        })
    
    return songs


def get_user_artist_songs():
    url = f'https://api.deezer.com/user/{user_id}/artists'
    headers = {'Authorization' : 'Bearer ' + deezer_token}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    songs = []
    
    # Go over to the artist list 
    for artist in data['data']:
        # Get the tracklist of artist
        tracklist = artist['tracklist']

        # GET to the tracklist of the artist. I put a params to get the first 10 songs
        tracklist_response = requests.get(tracklist, params={'limit':10})
       
        if tracklist_response.status_code == 200:
            tracklist_data = tracklist_response.json()
            
            # Get the song list from the tracklist
            tracks = tracklist_data['data']

            for track in tracks:
                songs.append({
                    'id': track['id'],
                    'title':track['title'],
                    'artist': track['artist']['name'],
                    'link': track['link'],
                    'cover': track['album']['cover_xl']
                 })
        else:
            print('Error:', response.status_code)

    return songs


def get_user_playlist_songs():
    url = f'https://api.deezer.com/user/{user_id}/playlists'
    headers = {'Authorization' : 'Bearer ' + deezer_token}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    songs = []

    for playlist in data['data']:
        tracklist = playlist['tracklist']
        
        tracks_response = requests.get(tracklist)

        if tracks_response.status_code == 200:
            tracks_data = tracks_response.json()

            tracks = tracks_data['data']

            for track in tracks:
                songs.append({
                    'id':track['id'],
                    'title':track['title'],
                    'artist': track['artist']['name'],
                    'link': track['link'],
                    'cover': track['album']['cover_xl']
                 })

        else:
            print('Error:', response.status_code)

    return songs 



def get_popular_songs():
    url = f'https://api.deezer.com/chart'
    headers = {'Authorization' : 'Bearer ' + deezer_token}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    songs = []

    for song in data['tracks']['data']:
        songs.append({
            'id':song['id'],
            'title':song['title'],
            'artist':song['artist']['name'],
            'link': song['link'],
            'cover': song['album']['cover_xl']
        })
    
    return songs



def tweet(song):
    widget_url = f'https://widget.deezer.com/widget/dark/track/{song["id"]}'
    response = requests.get(song['cover'])
    with open('cover.jpg', 'wb') as f:
        f.write(response.content)
    
    album_cover = api.media_upload('cover.jpg')
    tweet_text = f"Hi 🖐️ Check this song 💿: \n{song['title']} by {song['artist']} \n {widget_url}"
    api.update_status(status=tweet_text, media_ids=[album_cover.media_id], auto_populate_reply_metadata=True)


    os.remove('cover.jpg')


while True:

     try:
        user_songs = get_user_songs()
        artist_songs = get_user_artist_songs()
        playlist_songs = get_user_playlist_songs()

        popular_songs = get_popular_songs()

        all_songs = user_songs + artist_songs + playlist_songs + popular_songs

        song = random.choice(all_songs)

        tweet(song)
       
      
        time.sleep(60 * 60 * 5)

     except Exception as e:
        print('Error: ', e)
        time.sleep(60 * 60)




