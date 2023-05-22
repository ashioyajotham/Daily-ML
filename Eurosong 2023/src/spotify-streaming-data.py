import secrets_spotify as ss
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import csv
import get_all_files_together as get_all

# Credentials to access Spotify API
client_id = ss.CLIENT_ID
client_secret = ss.CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Playlist ID (Eurovision 2023 - Playlist by Spotify)
playlist_id = '37i9dQZF1DWVCKO3xAlT1Q'

# Get all songs from playlist
results = sp.playlist_tracks(playlist_id)
tracks = results['items']
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

# Extract URIs of all songs composing the playlist
uris = [track['track']['uri'] for track in tracks]

# Obtaining tracks data and sorting it by field popularity (indicator of streaming count)
sorted_tracks = sorted(uris, key=lambda uri: sp.track(uri)['popularity'], reverse=True)

# Creating list of lists and including the header of the final CSV file 
spotify_data = []
head = ['date', 'position', 'song', 'artist', 'popularity']
spotify_data.append(head)
today = datetime.today().strftime('%Y-%m-%d')

# Getting the data obtained from Spotify API into the list of lists
for rank, uri in enumerate(sorted_tracks):
    track = sp.track(uri)
    name = track['name']
    popularity = track['popularity']
    total_tracks = track['album']['total_tracks']
    artist = track['album']['artists'][0]['name']
    spotify_data.append([today, rank+1, name, artist, popularity])

## Pass data into a csv file
csv_file = open('./data/spotify/' + today + '-spotify-streaming.csv', 'w', encoding="utf-8", newline='')
writer = csv.writer(csv_file)
for data_list in spotify_data:
    writer.writerow(data_list)
csv_file.close()

## Create combined file (all data)
get_all.get_all_files_together("./data/spotify", "./all", "eurovision-spotify-streaming.csv")