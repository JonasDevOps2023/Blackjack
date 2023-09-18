import platform
import requests
import json
import os


url = "https://5hyqtreww2.execute-api.eu-north-1.amazonaws.com/artists/"

artists = ''

os_name = platform.system()

def get_artists_json():
    return json.loads(requests.get(url).text)

def get_artist_info(artist):
    return json.loads(requests.get(url + artist["id"]).text)

def return_artist_info(name):
    for artist in get_artists_json()["artists"]:
        if artist["name"].lower() == name.lower():
            return get_artist_info(artist)["artist"]
    return None

def enter_to_continue():
    input("press enter to continue")

def clear_console():
    if os_name == "Windows":
        os.system('cls')
    elif os_name == "Linux" or os_name == "Darwin":
        os.system('clear')


clear_console()
print(f"You're running on {os_name}")
while True:
    print("--- ARTIST DB ---")
    for artist in get_artists_json()["artists"]:
        print(artist["name"])
    print('-----------------')
    print("Select artist")
    choice = input("> ")
    if choice.lower() == "quit":
        print("Exiting....")
        break
    artist_info = return_artist_info(choice)
    if not artist_info == None:
        print('-----------------')
        print(artist_info["name"])
        print("*****************")
        print(", ".join(artist_info["genres"])) 
        print(", ".join(artist_info["years_active"]))
        print(", ".join(artist_info["members"]))
        print('-----------------')
        enter_to_continue()
        clear_console()
    else:
        clear_console()
        print(f"Artist \"{choice.upper()}\" does not exist")
        enter_to_continue()
        clear_console()





#for artist in get_artists_json()["artists"]:
#a    print(artist["name"])

"""
--- ARTIST DB ---
Ariana Grande
Avicii
Blink -182
Brad Paisley
Ed Sheeran
Imagine Dragons
Maroon 5
Scorpions
-----------------
Select artist :
> avicii
-----------------
Avicii
*****************
Genres : progressive house , electro house
Years active : 2006 -2018
Members : Tim Bergling
-----------------
"""




#Public-apis
