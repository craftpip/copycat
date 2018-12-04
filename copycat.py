import random
import spotipy
import urllib.request
from spotipy.oauth2 import SpotifyClientCredentials
import os
import argparse
import youtube_dl
import subprocess
from youtube import API
import eyed3
import urllib
import requests
from pyquery import PyQuery as pq
import threading
import time
import shutil
import sys
from bs4 import BeautifulSoup

configs = {
    'threads': 4,  # use this many downloads at once! super duper fast! consumes CPU like its cake!
    'concurrent_connections': 4,
    'download_dir': 'D:/Music/',  # copy the playlists in here
    'sync_download_dir': [  # list of my sync directories, if you ha
        'G:/MUSIC/spotify/'
    ],
    'song_selection': {
        'edge_cases': ['remix', 'live', 'instrumental', 'cover', 'how to', 'tutorial', 'concert', 'karaoke', 'perfomance', '8D', 'Chipmunks', 'bass boosted'],  # download anything except this, only if the required song does not contain these words.
        'min_percent_threshold': 80,  # if a song title is more than 5 words, check if % if it matches
        'diff_track_seconds_limit': 5,  # limit duration comparision for top 2 songs
        'append_search_term': '',  # append some terms for search
    },
    'youtube_username': None,  # Cant download ? try this
    'youtube_password': None,
    'tag_mp3': True,  # sure, why would you not?
    'sleep_timer_minutes': 15,  # use -r and restart copycat after 15 minutes
    'spotify': {  # you know what
        'client_id': 'ea59966691f546a38c800e765338cf31',
        'client_secret': 'a99b13c2324340939cca0a6d71f91bc3'
    },
    'playlist': {
        'spotify_parsed': [],  # for internal use, dont worry
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
            'spotify:user:swissendo:playlist:2RjVgOpvTms8WmlHC93bxU',
            'spotify:user:123081956:playlist:6pbOuIfOAMVSYxV9FIBvsI',
            'spotify:user:jlfgaming:playlist:5PkNSRODWEvFIp4u8mHZXH',
            'spotify:user:21xpqeodpx4vlobjtdxf6xt3y:playlist:1T00fgjM0Epc6MunxsmrA7',
            'spotify:user:pewdie:playlist:4qJBhPqsmoqwV7mPsgJZ6l',
            'spotify:user:22gfazgq7twsmgidqrpzablla:playlist:1nJkQ7YbenUXPliKUYHH8k',
            'spotify:user:goldenavatar1:playlist:60m43P0UjaLrmI9XdCZmuF',
            'spotify:user:zs0qpp1zt836hy3qscmipn38y:playlist:5tTlPOZIr4EaV42OUiJAcZ',
            'spotify:user:zs0qpp1zt836hy3qscmipn38y:playlist:33iJTZ55XEWs2zPHTKpRCq',
            'spotify:user:cliff9810:playlist:0KiOJjW21jHFWryuFu8EHi',
            'spotify:user:pewdie:playlist:0FjMXxjLKm9DIwYMVUrX3i',
            'spotify:user:tdq7bo60ro67xx9gnuatz1qx6:playlist:0FSkZ3y8AV6VZU49F31sRT',
            'spotify:user:pewdie:playlist:1qWIvsjfa2V69YiuME2zJM',
            'spotify:user:21g7fr65qebg7ritookvwlloa:playlist:6eNQ20tCDoxguQ6yp1aQ8w',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:0tkQu3nGrfoxmK33pdMDoS',
            'spotify:user:21pvzacbrr6h6awhrfzqmhlnq:playlist:3X4oLrVQfB6i44z3aJDIxl',
            'spotify:user:21pvzacbrr6h6awhrfzqmhlnq:playlist:7hYrzrl2TbVF4aEpnVHqgG',
            'spotify:user:21pvzacbrr6h6awhrfzqmhlnq:playlist:0OtZSHd8rFgNDtBwtQbyCZ',
            'spotify:user:11179003172:playlist:7fBRvz6S4mjswDjUmaK4hq',
            'spotify:user:11179003172:playlist:5zDcKzdZaqjs4o4zf9x0wp',
            'spotify:user:joshtunji:playlist:0X0Vnaf0XaeE8MqoAUATMy',
            'spotify:user:wiks69g0l47jxtgm7z1fwcuff:playlist:6qHGCjoXAIGKVsg0rNdAMh',
            'spotify:user:madelenee.:playlist:1vuGNDn807qM1Qsa1fUfZq',
            'spotify:user:beckz:playlist:6ZZnxExyWOOE8GavGSNHIB',
            'spotify:user:daniel_lawson9999:playlist:6jeSKyPBU24fdGlYfOaSnx',
            'spotify:user:spotify:playlist:37i9dQZF1DX5q67ZpWyRrZ',
        ]
    }
}

parser = argparse.ArgumentParser(description="Copy that shit")
parser.add_argument("-s", help="sync the playlist and with target drive", action='store_true')
parser.add_argument("-ds", help="sync with drive only", action='store_true')
parser.add_argument("-r", help="loop the process after 2 hrs", action='store_true')
parser.add_argument("-v", help="get more output?", action='store_true')
parser.add_argument("-d", help="For debug", action='store_true')
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

    try:
        response = urllib.request.urlopen(url)
        html = response.read()
        html = str(html, 'utf-8')
    except Exception as e:
        p('Youtube gave up! :( ' + repr(e))
        return []

    page = BeautifulSoup(html, features='lxml')
    vid_list = page.find_all('div', attrs={'class': 'yt-lockup-content'})

    # d = pq(html)
    # vid_list = d('.yt-lockup-content')
    video_list = []
    for vid in vid_list:

        title_link = vid.findChild('a', attrs={'class': 'yt-uix-tile-link'}, recursive=True)
        if title_link is None:
            continue

        title = title_link.attrs['title']
        href = title_link.attrs['href']

        # title = vid.('a', attrs={'class': 'yt-uix-tile-link'}).attrs['title']
        # title = vid.find('a', attrs={'class': 'yt-uix-tile-link'}).attrs['href']
        # title = vid.attrib['title']
        # href = vid.attrib['href']
        # if 'aria-describedby' in vid.attrib:
        #     des = vid.attrib['aria-describedby']
        # else:
        #     continue

        duration_el = vid.findChild('span', attrs={'class': 'accessible-description'}, recursive=True)
        if duration_el is None:
            continue

        duration = duration_el.text

        channel_name = ''
        channel_name_el = vid.findChild('a', attrs={'class': 'yt-uix-sessionlink'}, recursive=True)
        if channel_name_el is None:
            channel_name = channel_name_el.text

        video_description_el = vid.findChild('div', attrs={'class': 'yt-lockup-description'}, recursive=True)
        video_description = ''
        if video_description_el is not None:
            video_description = video_description_el.text

        # duration = d('#' + des).contents()[0]

        if duration.find('Duration') == -1:
            continue

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
            'channel': channel_name,
            'description': video_description,
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
    if configs['youtube_username'] is not None:
        ydl_opts['username'] = configs['youtube_username']
    if configs['youtube_password'] is not None:
        ydl_opts['password'] = configs['youtube_password']

    a = youtube_dl.YoutubeDL(ydl_opts)
    v = a.download(['https://www.youtube.com/watch?v=' + video_id])
    return './' + file_name + '.webm'


def convert_to_mp3(source, target):
    source = source.replace('/', '\\')
    target = target.replace('/', '\\')

    # fnull = open(os.devnull, 'w')
    # subprocess.call('.\\ffmpeg\\bin\\ffmpeg.exe -threads 6 -i "' + source + '" -vn -ab 128k -ar 44100 -y "' + target + '"', shell=True, stdout=fnull, stderr=subprocess.STDOUT)

    os.system(
        '".\\ffmpeg\\bin\\ffmpeg.exe -hide_banner -i "' + source + '" -vn -ab 128k -ar 44100 -y "' + target + '""')


def tag_mp3(file_path, track):
    f = eyed3.load(file_path)
    if f.tag is None:
        f.initTag()

    if track['album_art'] is not None:
        content = requests.get(track['album_art']).content
        f.tag.images.set(3, content, 'image/jpeg')

    # f.info

    f.tag.comments.set(track['search_term'] + ' = ' + track['selected_result'])
    f.tag.artist = track['artist']
    f.tag.album = track['album']
    f.tag.album_artist = track['artist']
    f.tag.title = track['name']
    f.tag.track_num = track['number']
    f.tag.save(None, (2, 3, 0))


def clean_filename(filename):
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-')
    filename = ''.join(filter(whitelist.__contains__, filename))
    filename = filename.lower().strip()
    return filename


get_spotify_playlist_threads = 0
get_spotify_playlist = []


def get_spotify_playlist(spotify_playlist):
    global get_spotify_playlist
    global get_spotify_playlist_threads
    get_spotify_playlist = []

    for playlist_info in spotify_playlist:
        def get_playlist(playlist_info2):
            global get_spotify_playlist_threads
            global get_spotify_playlist
            info = sp.user_playlist(playlist_info2['user'], playlist_info2['playlist_id']);

            owner_name = info['owner']['display_name']
            p('Got playlist from ' + owner_name + ' ' + info['name'])
            path = clean_filename(owner_name[:6] + '-' + info['name'])

            playlist_single_info = {
                'name': info['name'],
                'path': path + '/',
                'tracks': [],
                'playlist_id': info['id'],
                'type': 'spotify',
                'user_id': info['owner']['id'],
                'user_name': info['owner']['display_name']
            }

            get_spotify_playlist.append(playlist_single_info)
            get_spotify_playlist_threads -= 1

        while get_spotify_playlist_threads > configs['concurrent_connections']:
            time.sleep(.1)

        t = threading.Thread(target=get_playlist, args=(playlist_info,))
        t.daemon = True
        get_spotify_playlist_threads += 1
        t.start()

    while get_spotify_playlist_threads != 0:
        time.sleep(.2)

    return get_spotify_playlist


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
        album_name = t['track']['album']['name']
        path = clean_filename(artist_name + '-' + track_name)

        track_term = clean_filename(track_name)
        composed_terms = []
        term_index = 0
        for term in track_term.split(' '):
            term_index += 1
            if len(term) > 1:
                if term_index < 5:
                    composed_terms.append('"' + term + '"')  # make strict search for first 5 words
                else:
                    composed_terms.append('' + term + '')  # not so strict search for later words

        composed_term = clean_filename(artist_name) + ' ' + (' '.join(composed_terms))

        search_term = composed_term + ' ' + configs['song_selection']['append_search_term']
        track = {
            'name': track_name,
            'search_term': search_term,
            'artist': artist_name,
            'album': album_name,
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
        elif len(images) == 1:
            image = t['track']['album']['images'][0]['url']
        else:
            image = None

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
        try:
            os.remove(d)
            p('Removed file: ' + d)
            dirs = d[:d.rfind('/')]
            remove_dir_if_empty(dirs)
        except:
            p("Hmm could not remove the file or dir")

    t = len(files_to_add)
    for f in files_to_add:
        d = dest + f
        dirs = d[:d.rfind('/')]
        if not os.path.exists(dirs + '/'):
            p('Creating folder ' + dirs)
            os.makedirs(dirs)
        if not os.path.exists(dest + f):
            if not os.path.exists(source + f):
                p('The source file ' + f + ' does not exists')
            else:
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
        p('Removing folder because its empty ' + a)
        os.removedirs(a)


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


running_threads = 0
total_playlist_cd = 0
total_playlist = 0
total_tracks_cd = 0
total_tracks = 0


def p2(s):
    p('pl:' + str(total_playlist_cd) + '/' + str(total_playlist) + '-tracks:' + str(total_tracks_cd) + '/' + str(total_tracks) + ' - ' + s)


def clean_temp():
    p('Cleaning temp')
    files = os.listdir('./')
    for f in files:
        if f.find('.webm') > -1:
            p('Removing temp file: ' + f)
            os.remove('./' + f)


process_playlist_threads = 0
parsed_playlist = []


def process_playlist():
    hr = '───────────────────'
    p('Starting sync')
    parse_spotify_playlist_config()
    p('Download dir: ' + configs['download_dir'])

    if not os.path.exists(configs['download_dir']):
        p('The download directory does not exists')
        exit(1)

    clean_temp()

    p('Getting playlists')
    playlist = get_spotify_playlist(configs['playlist']['spotify_parsed'])

    global total_playlist
    global total_playlist_cd
    global total_tracks
    global total_tracks_cd
    global parsed_playlist
    parsed_playlist = []
    total_playlist = len(playlist)
    total_playlist_cd = total_playlist
    total_tracks = 0
    total_tracks_cd = 0
    p(hr)
    p('Found ' + str(total_playlist) + ' playlists')

    global process_playlist_threads
    process_playlist_threads = 0

    for pl in playlist:
        def get_playlist(pl2):
            global process_playlist_threads
            global total_tracks
            global parsed_playlist
            tracks = get_spotify_tracks(pl2['user_id'], pl2['playlist_id'])
            total_tracks += len(tracks)
            p('Got ' + str(len(tracks)) + ' tracks from ' + pl2['name'])
            pl2['tracks'] = tracks
            parsed_playlist.append(pl2)
            process_playlist_threads -= 1

        while process_playlist_threads > configs['concurrent_connections']:
            time.sleep(0.5)

        t = threading.Thread(target=get_playlist, args=(pl,))
        t.daemon = True
        process_playlist_threads += 1
        t.start()

    while process_playlist_threads != 0:
        time.sleep(0.5)

    p('Playlist scan complete, found ' + str(total_tracks) + ' total tracks')
    p(hr)
    total_tracks_cd = total_tracks

    diff_file_paths = []

    p2('Starting..')

    for pl in parsed_playlist:
        folder_path = configs['download_dir'] + pl['path']
        for track_index, track in enumerate(pl['tracks']):

            def process_track(pl, folder_path, track, track_index):
                global running_threads
                global total_tracks_cd
                running_threads += 1
                pre_text = pl['name'][:10] + ' | ' + track['name']
                p(hr + ' ' + pre_text)
                p2(str(running_threads) + 'T | ' + pre_text)
                diff_file_paths.append(pl['path'] + track['path'])
                file_path = folder_path + track['path']
                p2(str(running_threads) + 'T | ' + pre_text + ': output to: ' + file_path)
                if os.path.exists(file_path):
                    p2(str(running_threads) + 'T | ' + pre_text + ': file already exists, skipping')
                    total_tracks_cd = total_tracks_cd - 1
                    running_threads -= 1
                    sys.exit()

                search_term = track['search_term']
                p2(str(running_threads) + 'T | ' + pre_text + ': searching yt for ' + search_term)
                all_results = search_youtube(search_term)
                p2(str(running_threads) + 'T | ' + pre_text + ': got ' + str(len(all_results)) + ' results')

                # have to remove unrelated results!!!
                # we are selecting wrong tracks because of the diff.
                # sometimes the diff of unrelated songs match exactly.
                terms = clean_filename(track['artist'] + ' ' + track['name'])
                terms_list = terms.split(' ')
                required_matched_terms = []
                for t in terms_list:
                    if len(t) > 1:
                        required_matched_terms.append(t)

                results = []
                required_matches = len(required_matched_terms)
                for r in all_results:
                    matches = 0
                    search_in = r['title'] + ' ' + r['channel'] + ' ' + r['description']
                    unrelated = False
                    r2 = clean_filename(search_in).lower()
                    for t in terms_list:
                        t2 = clean_filename(t).lower()
                        if len(t) > 1 and r2.find(t2) != -1:
                            matches += 1

                    if required_matches < 5 and matches != required_matches:
                        unrelated = True
                    elif required_matches >= 5:
                        # if a song has a long name, considering words beyond 5 are long,
                        # then percent will be calculated, more than n% will qualify
                        required_words_to_matches = configs['song_selection']['min_percent_threshold'] * required_matches / 100
                        if matches < round(required_words_to_matches):
                            unrelated = True

                        # match_percent = matches * 100 / required_matches
                        # if match_percent < configs['song_selection']['min_percent_threshold']:  # matches less than 60 percent will disqualify

                    # detect edge cases here live, instrumental etc
                    edge_cases = configs['song_selection']['edge_cases']
                    for e in edge_cases:
                        if r2.find(e) != -1 and terms.find(e) == -1:
                            unrelated = True
                            break

                    if not unrelated:
                        results.append(r)

                # compare the first X no. of  tracks ? and check for the lowest difference in duration
                def select_result(re):
                    lowest_index = 0
                    lowest_diff = 1000
                    for index, r in enumerate(re):
                        diff = abs(int(r['duration_seconds']) - int(track['duration']))
                        if diff < lowest_diff and index < configs['song_selection']['diff_track_seconds_limit']:
                            lowest_diff = diff
                            lowest_index = index

                    p2(str(running_threads) + 'T | ' + pre_text + ': length diff = ' + str(lowest_diff) + ' seconds')
                    p2(str(running_threads) + 'T | ' + pre_text + ': selecting = "' + re[lowest_index]['title'] + '"')
                    return [lowest_index, lowest_diff]

                if len(results) == 0:
                    p2(str(running_threads) + 'T | ' + pre_text + ': results were not found')
                    total_tracks_cd = total_tracks_cd - 1
                    running_threads -= 1
                    sys.exit()

                sr = select_result(results)
                result_index = sr[0]
                result_diff = sr[1]
                selected_result = results[result_index]
                try:
                    p2(str(running_threads) + 'T | ' + pre_text + ': downloading audio')
                    video_path = download_video(selected_result['video_id'], track['path'])
                except:
                    # one more try.
                    p2(str(running_threads) + 'T | ' + pre_text + ':failed to download, one more try?')
                    results.pop(result_index)
                    sr = select_result(results)
                    result_index = sr[0]
                    result_diff = sr[1]
                    selected_result = results[result_index]
                    p(str(running_threads) + 'T | ' + pre_text + ':could not download video, selecting different one')
                    try:
                        video_path = download_video(selected_result['video_id'], track['path'])
                    except:
                        p2(str(running_threads) + 'T | ' + pre_text + ':failed to download the song again, giving up!')
                        running_threads -= 1
                        sys.exit()

                # this was the selected result
                track['selected_result'] = selected_result['video_id'] + ' ' + selected_result['title'] + ' I:' + str(result_index) + ' D:' + str(result_diff)

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # def in_thread():
                p2(str(running_threads) + 'T | ' + pre_text + ': converting to mp3')
                convert_to_mp3(video_path, file_path)
                time.sleep(.1)
                os.remove(video_path)

                if configs['tag_mp3']:
                    p2(str(running_threads) + 'T | ' + pre_text + ': downloading album art')
                    p2(str(running_threads) + 'T | ' + pre_text + ': adding meta-data to mp3')
                    tag_mp3(file_path, track)
                    p2(str(running_threads) + 'T | ' + pre_text + ': saved to ' + file_path)

                total_tracks_cd = total_tracks_cd - 1
                running_threads -= 1

            while running_threads > configs['threads'] - 1:
                time.sleep(.01)

            # time.sleep(random.uniform(0, 1))
            t = threading.Thread(target=process_track, args=(pl, folder_path, track, track_index))
            t.daemon = True
            t.start()

        total_playlist_cd -= 1

    p('Waiting for threads to finish :' + str(running_threads))
    while running_threads != 0:
        print('... Running threads: ' + str(running_threads))
        time.sleep(1)

    p('Checking for removed files')
    diffed_files = diff_files(configs['download_dir'], configs['download_dir'], files=diff_file_paths)

    if len(diffed_files['files_to_remove']):
        p('Removing files')
        process_diff_files(diffed_files, configs['download_dir'], configs['download_dir'])

    sync_drive()

    if args.r:
        p('Restarting sync in ' + str(configs['sleep_timer_minutes']) + ' minutes')
        time.sleep(configs['sleep_timer_minutes'] * 60)
        process_playlist()


def sync_drive():
    for drive in configs['sync_download_dir']:
        if os.path.exists(drive):
            p('Syncing files with ' + drive)
            drive_diff_files = diff_files(configs['download_dir'], drive)
            process_diff_files(drive_diff_files, configs['download_dir'], drive)
        else:
            p('The path ' + drive + ' does not exists atm, skipping')


if args.d:
    print('ok')
    results = search_youtube('+Cocainejesus +She')
    # tag_mp3('./tracks/1/airbag-colours.mp3', {})

if args.s:
    process_playlist()

if args.ds:
    sync_drive()
