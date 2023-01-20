import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def read_config(key):
    with open('config.json') as f:
        config = json.load(f)
    return config[key]


def login(client_id, client_secret):
    return spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
    )


if __name__ == "__main__":
    spotify = login(read_config('CLIENT_ID'), read_config('CLIENT_SECRET'))
    results = spotify.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
