import tweepy
import requests
import json 


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

user_id = 729578273

def get_song_user():
    url = f'https://api.deezer.com/user/{user_id}/tracks'
    headers = {'Authorization' : 'Bearer ' + deezer_token}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    songs = data['data']
    return songs


def get_song_artist():
    url = f'https://api.deezer.com/user/{user_id}/artists'
    headers = {'Authorization' : 'Bearer ' + deezer_token}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    songs = []
    
    # Go over to the artist list 
    for song in data['data']:
        # Get the tracklist of artist
        tracklist = song['tracklist']

        # GET to the tracklist of the artist. I put a params to get the first 10 songs
        tracklist_response = requests.get(tracklist, params={'limit':10})
       
        if tracklist_response.status_code == 200:
            tracklist_data = tracklist_response.json()
            
            # Get the song list from the tracklist
            tracks = tracklist_data['data']

            songs.append({
                'tracks':tracks
            })
        else:
            print('Error:', response.status_code)

    return songs


def get_song_playlist():
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

            songs.append({
                'tracks':tracks
            })
        else:
            print('Error:', response.status_code)

    return songs 



def get_popular_songs():
    url = f'https://api.deezer.com/chart'
    headers = {'Authorization' : 'Bearer ' + deezer_token}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    songs = data['tracks']['data']
    return songs

popular_songs = get_popular_songs()
print(popular_songs)