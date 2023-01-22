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
    if read_config("playlist_id") == "" \
            or sp.playlist_items(read_config("playlist_id"), limit=read_config("max_songs"))['total'] == 0:
        
        logging.info("Creating new playlist...")
        
        playlist = sp.user_playlist_create(user=sp.me()['id'],
                                           name=read_config("playlist_name"),
                                           public=read_config("is_public"),
                                           collaborative=False,
                                           description=read_config("playlist_description"))
        
        set_config("playlist_id", playlist['id'])
        
    return sp.playlist_items(read_config("playlist_id"), limit=read_config("max_songs"))


def compare_playlists(liked_playlist, playlist):
    is_same = False
    for idx_liked, item_liked in enumerate(liked_playlist['items']):
        for idx_playlist, item_playlist in enumerate(playlist['items']) if playlist else enumerate([]):
            # If the liked song is in the playlist and the index is the same, it's the same playlist
            if item_liked['track']['id'] == item_playlist['track']['id'] and idx_liked == idx_playlist:
                is_same = True
    logging.debug(f"Is same Playlist?: {is_same}")
    return is_same


if __name__ == "__main__":
    logging.debug("Logging into Spotify...")

    spotify = login(read_config('CLIENT_ID'),
                    read_config('CLIENT_SECRET'),
                    read_config('REDIRECT_URI'),
                    read_config('SCOPE'))
    login_time = datetime.datetime.now()

    logging.info(f"Logged in at {login_time}!")

    while True:
        # If the token is expired, login again
        if datetime.datetime.now() > login_time + datetime.timedelta(seconds=read_config("token_expiration")*60):
            logging.debug("Token expired, logging in again...")
            spotify = login(read_config('CLIENT_ID'),
                            read_config('CLIENT_SECRET'),
                            read_config('REDIRECT_URI'),
                            read_config('SCOPE'))
            login_time = datetime.datetime.now()
            logging.info(f"Logged in at {login_time}!")

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
                                           [item_liked['track']['uri'] for item_liked in liked_songs['items']])
            logging.info(f"Playlist updated at {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}!")

        logging.info("Next Check: " + (
                    datetime.datetime.now() + datetime.timedelta(minutes=read_config("refresh_time"))).strftime(
            '%d-%m-%Y %H:%M:%S'))
        time.sleep(read_config("refresh_time") * 60)
