# Twitchmusic-Spotify-Playlist-Creator
## Creating spotify playlist from twitch streamer songlist 

Twitch Music streamers mostly use [streamersonglist](https://www.streamersonglist.com/) to manage their songlist . 

Use this tool to convert twitch music songlists to a spotify playlist on your account . 

Download the tool (Twitchmusic_spoitfy_playlist_creator.exe and config.txt file) from the Github repo [releases](https://github.com/akhilmaddineni/Twitchmusic-Spotify-Playlist-Creator/releases) section .

After downloading the tool , Edit the config.txt file to fill out all the necessary info . 

In config.txt , please fill out all the necessary info as shown below , Edit the necessary parameters as needed  : 
```
# streamer name on twitch
streamer_id = cornyears

# streamer name on spotify -> for original songs
streamer_name_spotify = Bethan Le Mas

# Artist name in songlist for streamer original songs eg.Original,cornyears etc:-
streamer_name_songlist = Original

# playlist name that you want to create
playlist_name = Cornyears songlist

# playlist description
playlist_description = Cornyears twitch songlist

# spotify details

# Spotify cilent ID is 11 digit unique id that can be found at account overview : https://www.spotify.com/in-en/account/overview
# Example  : spotify_client_id =12345678901
spotify_client_id =

# Spotify token can be generated at : https://developer.spotify.com/console/post-playlists/
# In this page click on get token and copy the token to the below variable
# while creating the token give permission to playlist create public field to create playlist on your account
# Example spotify_secret = someUniQueKeyFromSpotify
spotify_secret =
```
After all the necessary parameters are filled in config.txt file , run Twitchmusic_spoitfy_playlist_creator.exe to create a spotify playlist from streamer's songlist . 

songs_not_found.csv will be generated for any songs that were not found by the program on spotify .

### How to run the repo locally

Prerequsites :- 
1. Python 3 
2. `pip install -r requirements.txt`

After editing the config.txt with the required parameters , run `python main.py` to create spotify playlist from the streamers song list . 
