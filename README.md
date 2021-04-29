# Copycat 

Copycat downloads your spotify playlists and syncs it on your local drive.

:heart: spotify     
v1.0.0

As working in an IT company we dont have access to our phones on work, that means no spotify, 
i have no choice but to keep my walkman in sync with my playlists, which gets boring after a while.
this tools does it for me, downloads the songs adds ID3 tags and keeps the download folder in sync with my walkman, 
finally i can live in peace.

## Flow?

- Reads your spotify playlist 
- Searches each track on youtube
- Downloads the best available audio format of the song that has the least difference in play length (and other factors for selection)
- Converts the file to mp3
- Adds ID3 tags and albumart to it
- Makes an exact copy of your playlists as folders on disk
- Syncs the playlist folders with a target drive (my walkman)
- Easy.


## Installation

Download the repo  
and install its dependencies
```cmd
pip install bs4
pip install eyed3
pip install spotipy
pip install youtube_dl
pip install lxml
```

Open `copycat.py` and make your customizations in the configs dict.

## Run it

```cmd
python copycat.py -s
```

## Authors

[Boniface Pereira](https://github.com/craftpip)

## Issues

Please post issues and feature request here [Github issues](https://github.com/craftpip/copycat/issues)

## Version changes
Versions are not yet maintained, working on master copy directly

## License

What