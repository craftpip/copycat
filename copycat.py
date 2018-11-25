import spotipy
import urllib.request
from spotipy.oauth2 import SpotifyClientCredentials
import os
import argparse
import youtube_dl
import subprocess
import eyed3
import urllib
import requests
from pyquery import PyQuery as pq
import threading
import time
import shutil

configs = {
    'download_dir': './tracks/',
    'sync_download_dir': 'G:/MUSIC/spotify/',
    'diff_track_seconds_limit': 3,
    'sleep_timer_minutes': 15,
    'append_search_term': '',
    'spotify': {
        'client_id': 'ea59966691f546a38c800e765338cf31',
        'client_secret': 'a99b13c2324340939cca0a6d71f91bc3'
    },
    'playlist': {
        'spotify_parsed': [],
        'spotify': [
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:7LcwHqdf9iDky7Oe2VERvG',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:5kfIHgK2R4J00apbdw4IDI',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:1QwlIfoV399cUtG4zOBopB',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:2hOGqIV7Ew99mGDNenf4Ws',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:0SgbnYrhjHwGTiVE9iun9L',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:7sFqi9CSJ2Bq4bGV7J6QrP',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:5UQfaRkWVkjVQXA4pKnMcF',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:5xflzpmFIBkTfosAi8L2S9',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:2qw21OuDXsbLNl0A0Yq4y8',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:42qXqZxkKrrigw4lhQyQTu',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:5Q62orQBszxls0g2yxWN6X',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:0eY4C0q3SVnZWmQiYSyTb3',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:4MpUBMEDNqkseBKLuNgCMr',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:6H6AyGNcTQbjQeI9GmQ07m',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:5Fehnt4XGBQVkHO2NF2sv0',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:4PKUgBkj8MOiQwHj5pEmTL',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:6XYIIFFpGHYQ2EsBsv9aAk',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:6eZobcGfdT3TuMylwgV1Hx',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:3Di9PmF4sLLLoaUQ10qqEL',
            'spotify:user:spotify:playlist:37i9dQZF1DX87JE1B72J6C',
            'spotify:user:1282700495:playlist:1CJQ6mkmmsw3qQKXUGuxIP',
            'spotify:user:tdq7bo60ro67xx9gnuatz1qx6:playlist:0eXnwvcuq88A9w6TvDeNLw',
            'spotify:user:brettwhitford:playlist:6UEF0bpIUlVnbPyjrAgdcQ',
        ]
    }
}

parser = argparse.ArgumentParser(description="Copy that shit")
# parser.add_argument('-sync', '-s', action=search_youtube, nargs=0)
# parser.add_argument("--add_playlist_from_user", help="echo the string you use here", action='store_true')
parser.add_argument("-s", help="sync the playlist and with target drive", action='store_true')
parser.add_argument("-ds", help="sync with drive only", action='store_true')
parser.add_argument("-r", help="loop the process after 2 hrs", action='store_true')
parser.add_argument("-v", help="get more output?", action='store_true')
args = parser.parse_args()

client_credentials_manager = SpotifyClientCredentials(configs['spotify']['client_id'],
                                                      configs['spotify']['client_secret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Printer
def p(str):
    print(str)
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(str)


def search_youtube(text_to_search):
    query = urllib.parse.quote(text_to_search)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    d = pq(html)
    vid_list = d('.yt-uix-tile-link')
    video_list = []
    for vid in vid_list:
        title = vid.attrib['title']
        href = vid.attrib['href']
        if 'aria-describedby' in vid.attrib:
            des = vid.attrib['aria-describedby']
        else:
            continue

        duration = d('#' + des).contents()[0]
        if duration.find('Duration') != -1:
            duration_parsed = duration[duration.find(':') + 2:-1]
            # not parsing hour long stuff right now: example: 1:01:49
            if len(duration_parsed) > 5:
                duration_parsed = '59:59'

            duration_in_seconds = int(duration_parsed[int(duration_parsed.find(':')) + 1:])
            duration_in_minutes = int(duration_parsed[:duration_parsed.find(':')])
            total_duration_in_seconds = duration_in_seconds + (duration_in_minutes * 60)
            video_id = href[href.find('?v=') + 3:]
            video_list.append({
                'title': title,
                'href': href,
                'video_id': video_id,
                'duration': duration_parsed,
                'duration_seconds': total_duration_in_seconds
            })
    return video_list


def sort_key(val):
    return val['duration_seconds']


def spotify_get_playlist_info(playlist):
    print(playlist)


def download_video(video_id, file_name):
    ydl_opts = {
        'format': '251/best',
        'outtmpl': './' + file_name + '.webm',
    }
    a = youtube_dl.YoutubeDL(ydl_opts)
    v = a.download(['https://www.youtube.com/watch?v=' + video_id])
    return './' + file_name + '.webm'


def convert_to_mp3(source, target):
    source = source.replace('/', '\\')
    target = target.replace('/', '\\')

    fnull = open(os.devnull, 'w')
    subprocess.call('.\\ffmpeg\\bin\\ffmpeg.exe -threads 6 -i "' + source + '" -vn -ab 128k -ar 44100 -y "' + target + '"', shell=True, stdout=fnull, stderr=subprocess.STDOUT)

    # os.system(
    #     '".\\ffmpeg\\bin\\ffmpeg.exe -i "' + source + '" -vn -ab 128k -ar 44100 -y "' + target + '""')


def tag_mp3(file_path, track):
    f = eyed3.load(file_path)
    if f.tag is None:
        f.initTag()

    content = requests.get(track['album_art']).content
    f.tag.images.set(3, content, 'image/jpeg')
    f.tag.artist = track['artist']
    f.tag.album = track['album']
    f.tag.album_artist = track['artist']
    f.tag.title = track['name']
    f.tag.track_num = track['number']
    f.tag.save()


def clean_filename(filename):
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-')
    filename = ''.join(filter(whitelist.__contains__, filename))
    filename = filename.lower().strip()
    return filename


def get_spotify_playlist(spotify_playlist):
    playlist = []

    for playlist_info in spotify_playlist:
        info = sp.user_playlist(playlist_info['user'], playlist_info['playlist_id']);

        playlist_single_info = {
            'name': info['name'],
            'path': clean_filename(info['name']) + '/',
            'tracks': [],
            'playlist_id': info['id'],
            'type': 'spotify',
            'user_id': info['owner']['id'],
            'user_name': info['owner']['display_name']
        }

        playlist.append(playlist_single_info)

    return playlist


def get_spotify_tracks(user_id, playlist_id):
    """
    tracks
    :param user_id:
    :param playlist_id:
    :return:
    """
    # @todo implement tracks gathering for more than 100 tracks, pagination pending
    tracks = sp.user_playlist_tracks(user_id, playlist_id, None, 100, 0)
    parsed_tracks = []
    for t in tracks['items']:
        track_name = t['track']['name']
        artist_name = t['track']['artists'][0]['name']
        path = clean_filename(artist_name + '-' + track_name)

        track = {
            'name': track_name,
            'artist': artist_name,
            'album': t['track']['album']['name'],
            'path': path + '.mp3',
            'number': t['track']['track_number'],
            'id': t['track']['id'],
            'duration': int(t['track']['duration_ms']) / 1000,
            'disc_number': str(t['track']['disc_number']),
            'artist_id': t['track']['artists'][0]['id'],
            'release_date': t['track']['album']['release_date'],
        }

        images = t['track']['album']['images']
        if len(images) > 1:
            image = t['track']['album']['images'][1]['url']
        else:
            image = t['track']['album']['images'][0]['url']

        track['album_art'] = image

        parsed_tracks.append(track)

    return parsed_tracks


def parse_spotify_playlist_config():
    playlist = configs['playlist']['spotify']

    for pl in playlist:
        user = pl[pl.find('user:') + 5:pl.find('playlist:') - 1]
        pl_id = pl[pl.find('playlist:') + 9:]
        configs['playlist']['spotify_parsed'].append({
            'user': user,
            'playlist_id': pl_id
        })


def process_diff_files(diff, source, dest):
    files_to_remove = diff['files_to_remove']
    files_to_add = diff['files_to_add']
    for r in files_to_remove:
        d = dest + r
        os.remove(d)
        dirs = d[:d.rfind('/')]
        remove_dir_if_empty(dirs)
        p('Removed file: ' + r)

    t = len(files_to_add)
    for f in files_to_add:
        d = dest + f
        dirs = d[:d.rfind('/')]
        if not os.path.exists(dirs + '/'):
            p('Creating folder ' + dirs)
            os.makedirs(dirs)
        if not os.path.exists(dest + f):
            p('Copying file ' + str(t) + '/' + str(len(files_to_add)) + ' - ' + dest + f)
            shutil.copyfile(source + f, dest + f)
        else:
            p('Already exists ' + str(t) + '/' + str(len(files_to_add)) + ' - ' + dest + f)
        t -= 1

    p('Files are in sync!')


def remove_dir_if_empty(a):
    files = os.listdir(a)
    if len(files) == 0:
        d = a[:a.rfind('/')]
        p('Removing folder because its empty ' + d)
        os.removedirs(d)


def diff_files(files_dir, compare_dir, files=None):
    dirs = os.listdir(compare_dir)

    if files is None:
        files = []
        f_dirs = os.listdir(files_dir)
        for d in f_dirs:
            f_files = os.listdir(files_dir + d)
            for f2 in f_files:
                files.append(d + '/' + f2)

    files_to_remove = []
    files_to_add = []

    for l in dirs:
        folder = l + '/'
        disk_files = os.listdir(compare_dir + folder)

        for df in disk_files:
            file = folder + df
            found = False
            for f in files:
                if file == f:
                    found = True
                    break

            if not found:
                files_to_remove.append(file)

    for f in files:
        exists = os.path.exists(compare_dir + f)
        if not exists:
            files_to_add.append(f)

    o = {
        'files_to_remove': files_to_remove,
        'files_to_add': files_to_add,
    }
    # print(o)
    return o


def process_playlist():
    hr = '============================================================================'
    p('Starting sync')
    parse_spotify_playlist_config()
    p('Download dir: ' + configs['download_dir'])

    p('Getting playlists')
    playlist = get_spotify_playlist(configs['playlist']['spotify_parsed'])
    parsed_playlist = []

    total_playlist = len(playlist)
    total_playlist_cd = total_playlist
    total_tracks = 0
    total_tracks_cd = 0
    p('Found ' + str(total_playlist) + ' playlists')

    for pl in playlist:
        p(hr)
        p('Getting tracks from ' + pl['name'])
        tracks = get_spotify_tracks(pl['user_id'], pl['playlist_id'])
        total_tracks += len(tracks)
        p('Got ' + str(len(tracks)) + ' tracks from ' + pl['name'])
        pl['tracks'] = tracks
        parsed_playlist.append(pl)

    p(hr)
    p('Playlist scan complete, found ' + str(total_tracks) + ' total tracks')
    total_tracks_cd = total_tracks

    def p2(s):
        p('pl:' + str(total_playlist_cd) + '/' + str(total_playlist) + '-tracks:' + str(total_tracks_cd) + '/' + str(total_tracks) + ' - ' + s)

    diff_file_paths = []

    p2('Starting..')
    for pl in parsed_playlist:
        folder_path = configs['download_dir'] + pl['path']
        for track_index, track in enumerate(pl['tracks']):

            p(hr)
            pre_text = pl['name'] + ' | ' + track['name']
            p2(pre_text)
            file_path = folder_path + track['path']

            diff_file_paths.append(pl['path'] + track['path'])

            p2(pre_text + ': output to: ' + file_path)
            if os.path.exists(file_path):
                p2(pre_text + ': file already exists, skipping')
                total_tracks_cd = total_tracks_cd - 1
                continue

            search_term = track['album'] + ' ' + track['artist'] + ' ' + track['name'] + ' ' + configs['append_search_term']
            p2(pre_text + ': searching yt for ' + search_term)
            results = search_youtube(search_term)
            p2(pre_text + ': got ' + str(len(results)) + ' results')

            # compare the first 5 tracks ? and check for the lowest difference in duration

            def select_result(results):
                lowest_index = 0
                lowest_diff = 1000
                for index, r in enumerate(results):
                    diff = abs(int(r['duration_seconds']) - int(track['duration']))
                    if diff < lowest_diff and index < configs['diff_track_seconds_limit']:
                        lowest_diff = diff
                        lowest_index = index

                p2(pre_text + ': length diff = ' + str(lowest_diff) + ' seconds')
                p2(pre_text + ': selecting = "' + results[lowest_index]['title'] + '"')
                return lowest_index

            if len(results) == 0:
                p2(pre_text + ': results were not found')
                total_tracks_cd = total_tracks_cd - 1
                continue

            result_index = select_result(results)
            selected_result = results[result_index]
            try:
                p2(pre_text + ': downloading audio')
                video_path = download_video(selected_result['video_id'], track['path'])
            except:
                # one more try.
                results.pop(result_index)
                result_index = select_result(results)
                selected_result = results[result_index]
                video_path = download_video(selected_result['video_id'], track['path'])
                p('could not download video, selecting different one')

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # def in_thread():
            p2(pre_text + ': converting to mp3')
            convert_to_mp3(video_path, file_path)
            time.sleep(1)
            os.remove(video_path)
            p2(pre_text + ': downloading album art')
            p2(pre_text + ': adding meta-data to mp3')
            tag_mp3(file_path, track)
            p2(pre_text + ': saved to ' + file_path)
            # global total_tracks_cd
            total_tracks_cd = total_tracks_cd - 1

            # t = threading.Thread(target=in_thread)
            # t.start()

        total_playlist_cd -= 1

    p('Checking for removed files')
    diffed_files = diff_files(configs['download_dir'], configs['download_dir'], files=diff_file_paths)

    if len(diffed_files['files_to_remove']):
        p('Removing files')
        process_diff_files(diffed_files, configs['download_dir'], configs['download_dir'])

    p('Syncing files with ' + configs['sync_download_dir'])
    drive_diff_files = diff_files(configs['download_dir'], configs['sync_download_dir'])
    process_diff_files(drive_diff_files, configs['download_dir'], configs['sync_download_dir'])

    if args.r:
        p('Restarting sync in ' + configs['sleep_timer_minutes'] + ' minutes')
        time.sleep(configs['sleep_timer_minutes'] * 60)
        process_playlist()


def sync_drive():
    drive_diff_files = diff_files(configs['download_dir'], configs['sync_download_dir'])
    process_diff_files(drive_diff_files, configs['download_dir'], configs['sync_download_dir'])


if args.s:
    process_playlist()

if args.ds:
    sync_drive()
