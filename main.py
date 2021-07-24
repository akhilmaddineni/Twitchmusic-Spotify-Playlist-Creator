import requests
from spotify_utils import CreatePlaylist
import re

#Reading the config.txt file

import configparser

config = configparser.RawConfigParser()
config.read('config.txt')
config_dict = dict(config.items('User_Config'))

print("*******************")
print(config_dict)
print("*******************")

url = config_dict['url']
streamer_id = config_dict['streamer_id'].rstrip()
rest_query = config_dict['rest_query']
response_limit = config_dict['response_limit']
streamer_name_songlist = config_dict['streamer_name_songlist'].rstrip()
streamer_name_spotify = config_dict['streamer_name_spotify'].rstrip()
spotify_client_id = config_dict['spotify_client_id'].rstrip()
spotify_secret = config_dict['spotify_secret'].rstrip()
playlist_name = config_dict['playlist_name']
playlist_description = config_dict['playlist_description']



rest_cmd_url = url + "/" + streamer_id + "/" + rest_query + "?" + response_limit
rest_api_response = requests.get(rest_cmd_url)

if rest_api_response.status_code != 200:
    raise Exception(
        "Communcation with REST API gone bad , please check error code {}".format(rest_api_response.status_code))

response_json = rest_api_response.json()
print(response_json)

# get the total number of songs in the songlist .
total_num_songs = response_json['total']
num_pages = total_num_songs // 100

songs_list = []
for i in range(num_pages + 1):
    rest_cmd_url_temp = rest_cmd_url
    rest_cmd_url_temp = rest_cmd_url + "&current=" + str(i)
    print(rest_cmd_url_temp)
    rest_api_response = requests.get(rest_cmd_url_temp)

    if rest_api_response.status_code != 200:
        raise Exception(
            "Communcation with REST API gone bad , please check error code {}".format(rest_api_response.status_code))

    response_json = rest_api_response.json()
    songs_list.extend(response_json['items'])

print(len(songs_list))

# filtering out the data
filtered_song_data = []


def remove_special_chars(text):
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    text = regrex_pattern.sub(r'', text)

    # remove text between two brackets
    text = re.sub("\(.*?\)", "", text)

    return text


def correct_original_artist_name(text):
    return text.replace(streamer_name_songlist, streamer_name_spotify)


for song_info in songs_list:
    filtered_song_data.append((remove_special_chars(song_info['title'].replace("'", r"\'")),
                               correct_original_artist_name(song_info['artist'].replace("'", r"\'"))))

print(filtered_song_data)

cp = CreatePlaylist(spotify_client_id, spotify_secret, filtered_song_data, playlist_name, playlist_description)
cp.add_to_playlist()
