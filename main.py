import json
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')


def read_config(key):
    with open('config.json') as f:
        config = json.load(f)
    return config[key]


def set_config(key, value):
    with open('config.json') as f:
        config = json.load(f)
    config[key] = value
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)


def login(client_id, client_secret, redirect_uri, scope):
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            open_browser=False
        )
    )


def get_playlist(sp):
    if read_config("playlist_id") == "" or \
            sp.playlist_items(read_config("playlist_id"), limit=read_config("max_songs"))['total'] == 0:
        logging.info("Creating new playlist")
        playlist = sp.user_playlist_create(user=sp.me()['id'], name=read_config("playlist_name"),
                                           public=read_config("is_public"),
                                           collaborative=False,
                                           description=read_config("playlist_description"))
        set_config("playlist_id", playlist['id'])
    return sp.playlist_items(read_config("playlist_id"), limit=read_config("max_songs"))


def compare_playlists(liked_playlist, playlist):
    is_same = False
    for idx, item in enumerate(liked_playlist['items']):
        for idx2, item2 in enumerate(playlist['items']) if playlist else enumerate([]):
            if item['track']['id'] == item2['track']['id'] and idx == idx2:
                is_same = True
    logging.debug(f"Is same: {is_same}")
    return is_same


# In config.json, if playlist_id is not set, it will create a new playlist!
if __name__ == "__main__":
    logging.debug("Logging into Spotify...")
    spotify = login(read_config('CLIENT_ID'),
                    read_config('CLIENT_SECRET'),
                    read_config('REDIRECT_URI'),
                    read_config('SCOPE'))
    logging.info("Logged in!")
    while True:
        logging.debug("Getting liked songs...")
        liked_songs = spotify.current_user_saved_tracks(limit=read_config("max_songs"))
        logging.info("Got liked songs!")
        logging.debug("Getting playlist...")
        playlist_songs = get_playlist(spotify)
        logging.info("Got playlist!")

        # Since I don't know if playlist_replace_items() will trigger the quota limit, I added a check
        logging.debug("Comparing playlists...")
        if compare_playlists(liked_songs, playlist_songs):
            logging.info("Playlist is up to date!")
        else:
            logging.info("Playlist is not up to date!")
            spotify.playlist_replace_items(read_config("playlist_id"),
                                           [item['track']['uri'] for item in liked_songs['items']])
            logging.info(f"Playlist updated at {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}!")

        logging.info("Next Check: " + (
                    datetime.datetime.now() + datetime.timedelta(minutes=read_config("refresh_time"))).strftime(
            '%d-%m-%Y %H:%M:%S'))
        time.sleep(read_config("refresh_time") * 60)
