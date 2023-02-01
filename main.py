import json
import time
import spotipy
import urllib3.exceptions
from spotipy.oauth2 import SpotifyOAuth
import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)


def read_config(key):
    with open("config.json") as f:
        config = json.load(f)
    return config[key]


def set_config(key, value):
    with open("config.json") as f:
        config = json.load(f)
    config[key] = value
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def login():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=read_config("CLIENT_ID"),
            client_secret=read_config("CLIENT_SECRET"),
            redirect_uri=read_config("REDIRECT_URI"),
            scope=read_config("SCOPE"),
            open_browser=False,
        )
    )


def get_playlist(sp):
    if (
        read_config("playlist_id") == ""
        or sp.playlist_items(
            read_config("playlist_id"), limit=read_config("max_songs")
        )["total"] == 0
    ):
        logging.info("Creating new playlist...")

        playlist = sp.user_playlist_create(
            user=sp.me()["id"],
            name=read_config("playlist_name"),
            public=read_config("is_public"),
            description=read_config("playlist_description"),
        )

        set_config("playlist_id", playlist["id"])

    return sp.playlist_items(read_config("playlist_id"), limit=read_config("max_songs"))


if __name__ == "__main__":
    logging.debug("Logging into Spotify...")
    spotify = login()
    login_time = datetime.datetime.now()
    logging.info(f"Logged in at {login_time}!")

    while True:
        # If the token is expired, login again
        if datetime.datetime.now() > login_time + datetime.timedelta(
            seconds=read_config("token_expiration") * 60
        ):
            logging.debug("Token expired, logging in again...")
            spotify = login()
            login_time = datetime.datetime.now()
            logging.info(f"Logged in at {login_time}!")

        logging.debug("Getting liked songs...")
        try:
            liked_songs = spotify.current_user_saved_tracks(
                limit=read_config("max_songs")
            )
        except urllib3.exceptions.ReadTimeoutError:
            logging.info("Timeout error, Logging in again...")
            spotify = login()
            login_time = datetime.datetime.now()
            logging.info(f"Logged in at {login_time}!")

            liked_songs = spotify.current_user_saved_tracks(
                limit=read_config("max_songs")
            )
        logging.info("Got liked songs!")

        logging.debug("Getting playlist...")
        playlist_songs = get_playlist(spotify)
        logging.info("Got playlist!")

        spotify.playlist_replace_items(
            read_config("playlist_id"),
            [item_liked["track"]["uri"] for item_liked in liked_songs["items"]],
        )
        logging.info(
            f"Playlist updated at {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}!"
        )

        logging.info(
            "Next Check: "
            + (
                datetime.datetime.now()
                + datetime.timedelta(minutes=read_config("refresh_time"))
            ).strftime("%d-%m-%Y %H:%M:%S")
        )
        time.sleep(read_config("refresh_time") * 60)
