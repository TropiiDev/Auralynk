from spotify.spotify_functions import *
from youtube.youtube_functions import *

first_token = get_spotify_token()
# I know this is recursive, and it will always generate a new token. I don't really care.
# I was just looking for something, so I can use it in the future.
token = get_valid_spotify_token(first_token)
filter = input("Song or Artist? ")
query = input("What song or artist? ")

if filter.lower() == "song":
    track = spotify_search_track(token, query)
    print(f"Song Name: {track['name']}, Artist: {track['artists'][0]['name']}")
    download_link = input("Do you want to download this song? (y/n) ")
    if download_link.lower() == "y":
        query = f"{track['name']} - {track['artists'][0]['name']}"
        link = search_youtube(query)
        file = download_audio(link)

        if file is not None:
            print(f"The file has been downloaded at {file}")
            print("Thank you for using Auralynk.")


elif filter.lower() == "artist":
    artist = spotify_search_artist(token, query)
    tracks_or_link = input("Do you want the top 10 tracks or links? (tracks/link) ")
    if tracks_or_link.lower() == "tracks":
        tracks = spotify_songs_by_artist(token, artist['id'])
        for idx, track in enumerate(tracks):
            print(f"{idx + 1}. {track['name']}")
    else:
        link = artist['external_urls']['spotify']
        print(f"Link: {link}")