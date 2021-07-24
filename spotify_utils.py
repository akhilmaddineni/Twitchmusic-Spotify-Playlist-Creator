import requests
import json


class CreatePlaylist:

    def __init__(self, user_id, token, song_tuples, playlist_name, playlist_description):
        self.user_id = user_id
        self.token = token
        self.tuples = song_tuples
        self.pl_name = playlist_name
        self.pl_desc = playlist_description

    # Step 1: Create playlist in Spotify.
    def create_playlist(self):
        request_body = json.dumps({
            "name": self.pl_name,
            "description": self.pl_desc,
            "public": True
        })
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )
        response_json = response.json()

        # playlist id
        return response_json["id"]

    # Step 2: Get each song's Spotify uri
    def get_spotify_uri(self, song, artist):
        try:
            query = "https://api.spotify.com/v1/search?query=track:%3A{}&type=track&offset=0&limit=1".format(
                song + " " + artist)
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.token)
                }
            )
            response_json = response.json()
            print(response_json)
            songs = response_json["tracks"]["items"]

            # URI
            uri = songs[0]["uri"]
        except Exception as e:
            print("Song Info not found in spotify Song %s , Artist %s " % (song, artist))
            uri = ""
        return uri

    def create_snf_csv_file(self, uri_not_found_list):
        with open("songs_not_found.csv", 'w') as f:
            f.write("SongName,ArtistName\n")
            for song_name, artist_name in uri_not_found_list:
                f.write(song_name + "," + artist_name + "\n")

    # Step 3: Add songs to Spotify Playlist
    def add_to_playlist(self):
        uris = []
        uri_not_found = []

        # Loop through tuples and get URIs
        for i, j in self.tuples:
            uri = self.get_spotify_uri(i, j)
            if uri != "":
                uris.append(uri)
            else:
                uri_not_found.append((i, j))

        # Create new playlist
        playlist_id = self.create_playlist()

        uris_100 = []
        if len(uris) > 100:
            uris_100 = uris[:100].copy()
        else:
            uris_100 = uris.copy()

        # Populate playlist
        request_data = json.dumps(uris_100)
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )

        response_json = response.json()
        # print(response_json)

        if len(uris) > 100:
            # populate the rest of the songs to the playlist
            divide_uri_list = [uris[i:i + 100] for i in range(0, len(uris), 100)]
            print(len(divide_uri_list))
            for i in range(1, len(divide_uri_list)):
                request_data = json.dumps(divide_uri_list[i])
                query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
                response = requests.post(
                    query,
                    data=request_data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer {}".format(self.token)
                    }
                )
                response_json = response.json()
                # print(response_json)

        # create a csv file for songs not found
        self.create_snf_csv_file(uri_not_found)

        return response_json
