<div align="center">

# Spotiply

[![Python][python-shield]][python-url]
[![Code style: black][black-shield]][black-url]
[![GitHub contributors][contributors-shield]][contributors-url] 
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

A Script that checks for your last liked songs on Spotify and adds it to a defined Playlist.
</div>

![](https://github.com/Luffy404/Spotiply/blob/main/.github/demo.gif)

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<div align="center">

## Installation

</div>

Use the Version Control System [git](https://git-scm.com) to install Spotiply.

```bash
git clone https://github.com/Luffy404/Spotiply
```

After that install all required python Libraries that can be found in requirements.txt.

On Windows:

```bat
py -m pip install -r requirements.txt
```

On Linux:

```bash
python3 -m pip install -r requirements.txt
```

Then configure config.json. You will require a Client ID and Client Secret which you can obtain on the [Developer Page of Spotify](https://developer.spotify.com/dashboard/).

You need to create a new application and edit the Settings. Under "Redirect URIs" you'll need to add the REDIRECT_URI found in [config.json](https://github.com/Luffy404/Spotiply/blob/main/config.json#L4) (It's set to "http://localhost" by default).

<div align="center">

## Usage

</div>

Run main.py

On Windows:

```bat
py main.py
```

On Linux:

```bash
python3 main.py
```

After that follow the Instructions that may appear in the Script.

<div align="center">

## Configuration

</div>

* "CLIENT_ID"
  * The client ID from Spotify
* "CLIENT_SECRET"
  * The client secret from Spotify
* "REDIRECT_URI"
  * The Redirect URI used by Spotify to authorize access.
* "SCOPE"
  * The scope your application will use.
  * [More Scopes can be found here](https://developer.spotify.com/documentation/general/guides/authorization/scopes/)
* "playlist_id"
  * The ID of the playlist that should get updated.
  * The ID is found in the URL if you copy your playlist.
  * If left empty or invalid a playlist will be generated.
* "playlist_name"
  * This value will be the Name of the playlist.
    * This will only take effect if no playlist is found.
* "playlist_description"
  * This value will be the description of the playlist.
    * This will only take effect if no playlist is found.
* "max_songs"
  * This value will define how many tracks will be added to the playlist.
* "refresh_time"
  * Time in minutes it waits until it compares the playlists.
* "is_public"
  * Defines if the playlist is set public.
    * This will only take effect if no playlist is found.
* "token_expiration"
  * Time in minutes the token will be valid.

<div align="center">

## Contributing

</div>

Pull requests, issue reports and feature requests are welcome. Any contributions are greatly appreciated.

<div align="center">

## License

</div>

[MIT](https://choosealicense.com/licenses/mit/)

[python-shield]: https://img.shields.io/badge/Python-3.9%20%7C%203.10-blue
[python-url]: https://www.python.org/downloads/
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://pypi.org/project/black
[contributors-shield]: https://img.shields.io/github/contributors/Luffy404/Spotiply.svg?style=flat-square
[contributors-url]: https://github.com/Luffy404/Spotiply/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Luffy404/Spotiply.svg?style=flat-square
[forks-url]: https://github.com/Luffy404/Spotiply/network/members
[stars-shield]: https://img.shields.io/github/stars/Luffy404/Spotiply.svg?style=flat-square
[stars-url]: https://github.com/Luffy404/Spotiply/stargazers
[issues-shield]: https://img.shields.io/github/issues/Luffy404/Spotiply.svg?style=flat-square
[issues-url]: https://github.com/Luffy404/Spotiply/issues
[license-shield]: https://img.shields.io/badge/License-MIT-yellow.svg
[license-url]: https://github.com/Luffy404/Spotiply/blob/main/LICENSE
