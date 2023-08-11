

import json
import requests
import os

API_KEY = "5c162fec6c36d6cd72d9618d786fd31c"

def GetAlbumTracks(mbid, name, artist):

    params = {
        "api_key": API_KEY,
        "format": "json",
        "method": "album.getinfo",
        "mbid": mbid,
        "album": name,
        "artist": artist
    }

    r = requests.get("http://ws.audioscrobbler.com/2.0/", params=params)

    tracks = []
    for track in r.json()["album"]["tracks"]["track"]:
        tracks.append({
            "name": track["name"],
            "duration": track["duration"]
        })

    return tracks

def Search(content, name, bonus_artist=None):
    
    params = {
        "api_key": API_KEY,
        "format" : "json",
        "method" : f"{content}.search",
        content  : name
    }
    if bonus_artist:
        params["artist"] = bonus_artist

    r = requests.get("http://ws.audioscrobbler.com/2.0/", params=params)

    return r.json()["results"][f"{content}matches"][content][0]

# def GetTrack(title, artist):
#     track = Search("track", title, artist)

#     info = {
#         "name": track["name"],
#         "artist": track["artist"]
#     }

#     path = os.getcwd()
#     SongPath = path + f"\\Spotify\\Songs"
#     if info['name'] not in os.listdir(SongPath):
#         os.mkdir(SongPath + "\\{info['name']}")

#     with open(SongPath + f"\\{info['name']}\\info.json", "w") as f:
#         json.dump(info, f, indent=4)

def GetAlbum(title, artist):
    album = Search("album", title, artist)

    info = {
        "name": album["name"],
        "artist": album["artist"],
        "image_url": album["image"][3]["#text"],
        "mbid": album["mbid"]
    }

    path = os.getcwd()
    AlbumPath = path + f"\\Albums"
    if info['name'] not in os.listdir(AlbumPath):
        os.mkdir(AlbumPath + f"\{info['name']}")
    
    tracks = GetAlbumTracks(info["mbid"], info["name"], info["artist"])
    info["tracks"] = tracks
    
    with open(AlbumPath + f"\\{info['name']}\\info.json", "w") as f:
        json.dump(info, f, indent=4)
    
    cover = requests.get(info["image_url"]).content
    with open(AlbumPath + f"\\{info['name']}\\cover.png", "wb") as f:
        f.write(cover)
    
    return info["name"]


def main():

    # choice = input("Track or Album?: ").lower()

    artist = input("Who is the artist?: ")
    
    # if choice == "track":
    #     title = input("What is the title of the track?: ")
    #     GetTrack(title, artist)

    # elif choice == "album":
    album = input("What is the title of the album?:")
    name = GetAlbum(album, artist)
    return "Albums", name


if __name__ == "__main__":
    main()


# Application name	Greenwood's Music Art
# API key	        5c162fec6c36d6cd72d9618d786fd31c
# Shared secret	    f5e2310d55d3141556ed9bc8912f5c09
# Registered to	Greenwood672