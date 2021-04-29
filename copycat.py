import argparse
import json
import os
import shutil
import sys
import threading
import time
import urllib
import urllib.request

import eyed3
import requests
import spotipy
import youtube_dl
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials

configs = {
    'threads': 12,  # use this many downloads at once! super duper fast! consumes CPU like its cake!
    'concurrent_connections': 2,  # threaded spotify connections,
    'download_dir': 'C:/Project/copycat/music/',  # Downloaded songs go here.
    'sync_download_dir': [  # Sync the downloaded songs with these directories
        'G:/MUSIC/spotify/',
    ],
    'song_selection': {
        'use_filtering': False,
        'edge_cases': ['remix', 'live', 'instrumental', 'cover', 'how to', 'tutorial', 'concert',
                       'reimagined', 'bass boost', 'boosted', 'explained', 'slowed', 'karaoke',
                       'datamosh', 'show', '3d', 'dance', 'unplugged', 'behind', 'festival',
                       'chipmunks', 'preview', 'mashup', 'feat', 'bass', 'acoustic', 'session',
                       ' vs ', 'sings', 'grammy', 'parody', 'decoded', 'lyrics',
                       'performance', '8d', 'chipmunks', 'bass boosted', 'clean'],
        # ignore songs that contain these words,
        'min_percent_threshold': 60,  # if a song title is more than 5 words, check if % if it matches
        'diff_track_seconds_limit': 5,  # limit duration comparision for top 2 songs
        'append_search_term': '',  # append some terms for search
    },
    'youtube_username': None,  # Cant download ? try this
    'youtube_password': None,  # 🙈
    'tag_mp3': True,  # sure, why would you not?
    'spotify': {  # you know what
        'client_id': 'ea59966691f546a38c800e765338cf31',
        'client_secret': 'a99b13c2324340939cca0a6d71f91bc3'
    },
    'playlist': {
        'spotify_parsed': [],  # for internal use, dont worry
        'spotify': [
            [
                'https://open.spotify.com/track/4yrloqLBKS7Pi3z7g2HDga?si=SFhC5k1qTLuf1ByrBlKWCA',
                'https://open.spotify.com/track/5EzGOkUwkRUXYAyvjlEHah?si=iJF3_Y-zQkKAhOLkhU6ScQ',
                'https://open.spotify.com/track/5rfNNdaCovygh3cxY1txTR?si=oIEDqPtERny1y0uAekcpVA',
                'https://open.spotify.com/track/4qRHWM6lESs5vqNmTJrhum?si=86y-wkA8QlyMi_dz1KMIrw',
                'https://open.spotify.com/track/56nziqLKNZ3METexiH6zdF?si=Dwak3g3HQNm1twoPkS-VGw',
                'https://open.spotify.com/track/0mXu9RFixtjgppxSvcYcYI?si=gO2c-7gpQNm3Ny_AYfnhoQ',
                'https://open.spotify.com/track/5j3iBuHq6vv7VcBo4Y2QrK?si=L1-hZJsMQBe0c2MN3MSOIA',
                'https://open.spotify.com/track/40mphbjHvSisMvIAmSfpBX?si=toJPcffsSLmfG5llqbIxgw',
                'https://open.spotify.com/track/5MjMvRHjOOIV6tA7OmC7mj?si=o7NtShzHRCWYoUMhMqNP4A',
                'https://open.spotify.com/track/4IiZlgVMQMM7yTVsgoF4n5?si=KZC_Cuk-Qoeg6NjHd5RXmw',
                'https://open.spotify.com/track/4U45aEWtQhrm8A5mxPaFZ7?si=LLmwJrYFRcuTR1w5zi_NpQ',
                'https://open.spotify.com/track/1bp2IO61zbQrbWNmKKxg3f?si=ItylzUeqTmC7NtFTsZyDtw',
                'https://open.spotify.com/track/1ne9wOtDF2jM6Cm8WBkaER?si=MEINsA2tTji4D73x1VYN9Q',
                'https://open.spotify.com/track/4NuYhskP3cjbKPKIzjs4ui?si=q8nGZmahSzGAoBBaMrBPWA',
                'https://open.spotify.com/track/37uGIrP6noERm2i7ECtMA7?si=IYBRlDyTRNKka22N7XFzNA',
                'https://open.spotify.com/track/539y2n1UYiM2gyYJKGNuuQ?si=m7dUZujhTEa-YscBsLGPRg',
                'https://open.spotify.com/track/3PZ0RoABbjIZhqvfFizOqa?si=BETn8jfjSF-dOWDTyDhs6A',
                'https://open.spotify.com/track/5Sl4KG5rsxTN5AIvSyz5rG?si=Duhm3g9cROifEeqxV8I02w',
                'https://open.spotify.com/track/26pC4BgyjdRIeieIcGqLcw?si=h5vDmkVLSDyv6Vv3A96tLQ',
                'https://open.spotify.com/track/7bliRZuMFa2JmUzzNd62kk?context=spotify%3Auser%3A1230996273%3Aplaylist%3A2zsz3v4L5Y1bYrSAToUux9&si=EAHXvBu9SMmoxX5t9K_wiA',
                'https://open.spotify.com/track/6w53UWYxXvQv5nU7GdNz1w?si=bbvVVdSVQLS8l-FJ3acuBQ',
                'https://open.spotify.com/track/4xa0M48GDJvxClxR1t6fTf?si=QWc71ACGSqCC-LlecAMtCA',
                'https://open.spotify.com/track/715fRwy0DoOnPbV6EMgcXt?si=f4htmbbBTMuQuZxz5cLoLQ',
                'https://open.spotify.com/track/3jNGLTOcA4a34rZD2y392C?si=oe1jihXGQnCodM9JfKTjOA',
                'https://open.spotify.com/track/3lWzVNe1yFZlkeBBzUuZYu?si=OWl1t2DLS0qTvl_Bmp1kPw',
                'https://open.spotify.com/track/3bH4HzoZZFq8UpZmI2AMgV?si=ljBJWmP5Stu3mIzpfjQqrA',
                'https://open.spotify.com/track/1oHLqcJbc9B7tVWlyCxq08?si=x6-9W8VrRoaNcIUWyu1R3A',
                'https://open.spotify.com/track/1kLXoAje5Z4mlZOAFgZZj3?si=H2U9GP5fR6Wvy2PwSPWFKg',
                'https://open.spotify.com/track/5A0sUMilD9HyM3UvMWk3zA?si=eUuvTplaQZuNvRqyn_PvEw',
                'https://open.spotify.com/track/13cUO19nAPFVL1KwAsp1uK?si=YxUMcHfRRWapXC67g0drng',
                'https://open.spotify.com/track/1Po2cMkzVblh10Lg3GimtJ?si=v1rbcrGRR5m_Xd8o4D1FQw',
                'https://open.spotify.com/track/5QrUUrMhPi8eLKLPKEI89v?si=4PJd3WVuTgeuKvy26g9GDA',
                'https://open.spotify.com/track/6nNWB2fwEbJHy7y587GV2M?si=S38KucqlQxaN2jB6Ib3nww',
                'https://open.spotify.com/track/5X0kkx0LFKtRyXYPSRjdc8?si=3n9Nk7jaT_G9vrqicrsXBQ',
                'https://open.spotify.com/track/5wakd1HmmslRhTcQMee8Mw?si=cpolWeUJRB-U0semhd0EIA',
                'https://open.spotify.com/track/0uWHS4k3dA4w5PQszKaZOp?si=eXhTKDeFS9-mymvOmQue5Q',
                'https://open.spotify.com/track/7mSmt2yar5VUXZNBV4AnpE?si=7lxcWkc0Q7iGD3ded_jLzA',
                'https://open.spotify.com/track/2Qpt0DpnjmpoTAWoiHf5d8?si=0hXbXlPwSCmO72mEh201-A',
                'https://open.spotify.com/track/5kgMPM2m2sGGuVL4KpHwiO?si=zSfkpL5cReGuVSdSrnfCZg',
                'https://open.spotify.com/track/69L4d5HlE0YOCwWFYVFGoW?si=6JGrijMDRtaJSOFZX2L89w',
                'https://open.spotify.com/track/11bD1JtSjlIgKgZG2134DZ?si=c-QGEeiVSJ6okb0YuqSNXw',
                'https://open.spotify.com/track/4iaGeV4WFvP2ynbqCIyTpS?si=q3kz2QI2RTC03hJTO18kig',
                'https://open.spotify.com/track/257SoE95qEweGItCB9Q5rE?si=DzVamVAPRh2AnPDpGuJmNg',
                'https://open.spotify.com/track/40RaUosMp8ROAFVeqrKZGw?si=5eCFlK_kTPuxeoNIkteUYA',
                'https://open.spotify.com/track/60CFGgbdZ315nIOuK5nYmM?si=LkkpSf6DQlGJKTsYfZtrBA',
                'https://open.spotify.com/track/6jj5kO7tFT3ir8WbbVO0iU?si=Wnxifhg1R2Go6jc-SvMw7A',
                'https://open.spotify.com/track/1rCPg5GOtes0FIo1BzgvUi?si=VjKsbeSZSCOLi0v9qaUiww',
                'https://open.spotify.com/track/57iDDD9N9tTWe75x6qhStw?si=3DKN0LzOS8-wfBBXm-uHdQ',
                'https://open.spotify.com/track/4iaGeV4WFvP2ynbqCIyTpS?si=W1Uq31ZzSk2deHGWgfzyhw',

                'https://open.spotify.com/track/0DbmsqP6basyejOSSh6MKP?si=SWW8mb9NRc6sAdEUygNm_A',
                'https://open.spotify.com/track/5fFqxdgVb6XRHN8VEoKh6I?si=_UDsJkpTSyyrPX6ANvkExw',
                'https://open.spotify.com/track/2lW2hWO7Xw1ADSUp50w9b5?si=ywSfe46aSkKLA6LNvzXzGQ',
                'https://open.spotify.com/track/16enJgtKy9yKQ9GEvzKBPI?si=qY-2TFCYTJCcGTpOUYO3YA',
                'https://open.spotify.com/track/3uIOxWVRZI2XaqHDXfDc9b?si=ljXcGCClQP66iID7ntuDIA',
                'https://open.spotify.com/track/71VqCMlnkqH1TYnRUk6IHG?si=S_GtRTNMQoahWBN9oRseDQ',
                'https://open.spotify.com/track/5u7s3ny0Qbzie63WMB3q2V?si=Po_1eopqQgewJhKgN0ceFw',
                'https://open.spotify.com/track/2k7aEpSZsvRSxif0JVPEaO?si=hfIDqD9cRfeM0gWP8aCscQ',
                'https://open.spotify.com/track/7EvKZAZ5Jnl8TxSuFrkEEZ?si=z4kha6OoQSGtBgbwhoIPew',
                'https://open.spotify.com/track/0YXCJlidjXsr7vnu7EXZtH?si=CiEjw4_CQPGQfneMEUCiSQ',
                'https://open.spotify.com/track/7oiMyI6ilKfrt01Q6aZdPl?si=IyBBj1MGTQKFyie5__cZ0Q',
                'https://open.spotify.com/track/504NLPDUBRylbZUUQR97XX?si=rp63v-NEQYGhoySbZexxTg',
                'https://open.spotify.com/track/54GVTQmVYDOEl0DclsMrz8?si=XHijIpx8QlSFpJCwYoLNTw',
                'https://open.spotify.com/track/5GcjIiSS47T64N1DFxn1UK?si=f0iWJPV4TKCSxaxeQ_PQLg',
                'https://open.spotify.com/track/2PyAVQqdVKGYr6ZFuODNLJ?si=LciD5SB9QFqciQwAKmeHmg',
                'https://open.spotify.com/track/44zGAo63hhc3xo0rlBweRo?si=C48Thm8LQQG1gZ3Ca1koGA',
                'https://open.spotify.com/track/2Z1HknKRrvUv5cheidF8Ag?si=l47dTfe7Rzyrb5HXSbjVqw',
                'https://open.spotify.com/track/2lW2hWO7Xw1ADSUp50w9b5?si=T1YP19sbQzWqScYIOZDH6g',
                'https://open.spotify.com/track/5Osd2BWeCNtA6EMLY0Dsil?si=sXF8RxFXQ-6BKBfsepIuuw',
                'https://open.spotify.com/track/0Qr61NXlyAeQaADO5xn3rI?si=WjbL-3LKTNum_xTBmzOepg',
                'https://open.spotify.com/track/7pKfPomDEeI4TPT6EOYjn9?si=y3GbETptSya3jaR9PfozDw',
                'https://open.spotify.com/track/2k7aEpSZsvRSxif0JVPEaO?si=E60hg5xuSe-K7X66azKW2w',
                'https://open.spotify.com/track/32aYOuHE2oj9v5JdujsOJ2?si=umbvwJ0CR4eZiGrSvnJ5EQ',
                'https://open.spotify.com/track/4e7qQOpigHBpRddCRB2BMi?si=gw3A9JeRTpCDr1ghY1Ho-w',
                'https://open.spotify.com/track/4ArKqELzF9JJ9ASW7MmqsO?si=Aho1508xQhuQzv4g-eOgHg',
                'https://open.spotify.com/track/62crJjeje0T8g5N3Tuq00V?si=WwwO5_H6QdqzjEkwvExEYQ',
                'https://open.spotify.com/track/6HuMrMrfhhVADQ67VMx61l?si=Y-_ElTW4SAWKWU5FRqZbyQ',
                'https://open.spotify.com/track/3rEUOhRcwfZEUVVSZjFiyG?si=Xgj0CH1WRz6K4phynP_kXA',
                'https://open.spotify.com/track/7fN3QQtmCMkiczQ41IuhwK?si=bTiGwFk8QEWNKe1KEiiVsg',
                'https://open.spotify.com/track/3YB9cvd668HXBEq8rbBW8P?si=8RYSR8nYSJ2kiwBpDQc-zA',
                'https://open.spotify.com/track/5OuJTtNve7FxUX82eEBupN?si=kJkUNGd7S-2nKy_XlBjp5g',
                'https://open.spotify.com/track/0hNhlwnzMLzZSlKGDCuHOo?si=0dzAf0Y6Q-qK-QxZ-wLEtA',
                'https://open.spotify.com/track/3p3O6XnkYZit3cECcvZyDe?si=whbYuUT_Ql67aTef8FkvLA',
                'https://open.spotify.com/track/4uAKeohK80UPEv8FWDTxvF?si=3Nm8W-UeSNa4s2neP25SPQ',
                'https://open.spotify.com/track/4QjDEMmKqBIbMCBETddJ3x?si=tlIZ6YSdQnizihHni41CPA',
                'https://open.spotify.com/track/3Rtv6zRNKpeSygXoaF9kCm?si=gLF76qSoTuyPKaXUjLrlyg',
                'https://open.spotify.com/track/5j3iBuHq6vv7VcBo4Y2QrK?si=_XBhWfrSRjWsAkUKwQidhA',
                'https://open.spotify.com/track/22kfxo7JTeqXbmjql43TIi?si=WBGn7jnbSpK-pODWrQ4rmw',
                'https://open.spotify.com/track/3PMQvsVUEOMWsEGsSGG0aA?si=0fnI-RG1SESVLSXYSgREHQ',
                'https://open.spotify.com/track/7u8MwUwM8oy3101vFMBMmp?si=Kzl54xq5R-yscJgDgzfH_g',
                'https://open.spotify.com/track/0iTpQYzJnYgh7kIxyq8A2O?si=5QHd4maGTGqNww24m4xVRw',
                'https://open.spotify.com/track/4KJHTdyIUdhKEuZdV3UuWR?si=sCaQohICRieE3l_9JQ_bIg',
                'https://open.spotify.com/track/6yw8KDkUJ468SsbKPlF1vA?si=POZRWiIzR2mH-XVjxN_EKg',
                'https://open.spotify.com/track/2lZHCWCUkxLuQ5skJhkoyS?si=PPPiaVvARW66w8_NoN2BUQ',
                'https://open.spotify.com/track/7rLq1Mdn1K50CiUAbCrwtI?si=tyAeEbDkSRq_gMDu-KXyXg',
                'https://open.spotify.com/track/1UmQrjcdTlI9pxT1gzU1Xa?si=R3bfmMw6QM2QBMI9diEGvQ',
                'https://open.spotify.com/track/7CcaktZZsdb8AWPdhDM38f?si=o4BXkTH6Q-iPdfKXZl-EAg',
                'https://open.spotify.com/track/75sAWnVBYaaYs1mWbB05Qg?si=12pcNFo4S9iKUbbEZzDfyw',
                'https://open.spotify.com/track/23qCHcGBR7VKLfUwq1r9iu?si=oxpDsE7AS2-DvH2vKWpxGA',
                'https://open.spotify.com/track/4tHqQMWSqmL6YjXwsqthDI?si=d54vHZlUTvy1tER3fOViPw',
                'https://open.spotify.com/track/6b0icYIM8HEaPvadDB3DEc?si=ARGjSH-dT9GDiJhC92g2Lg',
                'https://open.spotify.com/track/52ojopYMUzeNcudsoz7O9D?si=yIFAXRMlQFm5CBkFINCNNw',
                'https://open.spotify.com/track/5jEiI1kg97yFHpiGERSGJ3?si=8_EbrKZFSg6CKDhPO54GRg',
                'https://open.spotify.com/track/2BVUOGciUUUqOPSLtHwLGp?si=D6aW0pu6QI2yHvAC-oaewA',
                'https://open.spotify.com/track/6tXYVzmdR7l7yEXY11b2Hq?si=tzK-7pV5RpqQHe8LRjO7Tw',
                'https://open.spotify.com/track/5La0oCt8N3LZwfssCGzuZG?si=_WYpkTTXRdK29CDlOKy4Ow',
                'https://open.spotify.com/track/37b1KAbfOZeBzeMB0LGO3g?si=abdqLw4KT2aubTfo7mQYvQ',
                'https://open.spotify.com/track/3AHqaOkEFKZ6zEHdiplIv7?si=uPyiVtU0ShCb4N4GbJ_39w',
                'https://open.spotify.com/track/1qqg36GouAEweWsSDfTgTW?si=n9AhibEwT3iM_uO_qtoc3A',
                'https://open.spotify.com/track/0JWWEdHFYjUJcCtSWmF3P9?si=26APvhQDTEKqPSEO7TqpPg',
                'https://open.spotify.com/track/669PEr8I3wOswY8BANBpdh?si=YMI1z_0LQLuuY60tp0FJTA',
                'https://open.spotify.com/track/6xHlnkbGTtQaPvFJVIweaD?si=-yZjD-zXSVi6WsC0rp0diw',
                'https://open.spotify.com/track/2viNxee3uNcVXrXvwAUVir?si=07B3YzS-RM-WZsze_m865g',
                'https://open.spotify.com/track/4stm6lf1vQBSl7Eq4Npzr0?si=EGzzEKzPRj6fa5F_UOfQSQ',
                'https://open.spotify.com/track/2jrc5wSJd4NYsewjDsoNEa?si=zet3JLurScy6gVk86Inx9A',
                'https://open.spotify.com/track/4Sg5kugcA7G2dyFpok5Jyt?si=YIiTw1xiRX28kRByuhTZaw',
                'https://open.spotify.com/track/2R7MOnecy9f8YrEsIJhpTf?si=SMlmlIcmRQODc7S7JxneXA',
                'https://open.spotify.com/track/6N5WkgPIDoTdbCXyyIIKAv?si=8XEzbhu3QiaA0f5v8r9MCg',
                'https://open.spotify.com/track/5T9G49pXWTV7SHMSksvfL4?si=EIjAiWBpRIK1M8rvF__19g',
                'https://open.spotify.com/track/6tpZYMxcVhIjypOnk5eglk?si=Z7hxfe-oTq6iQFjiLCyL7g',
                'https://open.spotify.com/track/5Q58RkKyUafm15Syxg79DW?si=U4ZNrekgRD-fMsxs6WWi7Q',
                'https://open.spotify.com/track/7qEKqBCD2vE5vIBsrUitpD?si=xo4icAMASYW5DVSmHSPOUg',
                'https://open.spotify.com/track/4K9xid96G3YmIvQZXN9SXg?si=dkxKKKJbS12GF4tAutTpRw',
                'https://open.spotify.com/track/2FeYeAGexV851DsHdFsAmo?si=AlTgBcwuRga2AF2VEmNvLQ',
                'https://open.spotify.com/track/3MYCrt08Tuc6vkBCh7CnRs?si=yWDYJqOiSKO2DraHMNV3MA',
                'https://open.spotify.com/track/7qEKqBCD2vE5vIBsrUitpD?si=rSIFbazASSaHe0S8hJRj-Q',
                'https://open.spotify.com/track/6HGDxEtcoUsztb2xeVOXTP?si=U3pPX81JQs6VDCRl-RPu_w',
                'https://open.spotify.com/track/4PShfgy75bCYTWb6hNEMPe?si=k6jh3OhmRSuPa5CFI7RpoQ',
                'https://open.spotify.com/track/3WyvZJGxtORVdtOkNyHBJp?si=DNwjewncTbiIVzigbfenKQ',
                'https://open.spotify.com/track/0up9rhm9qt2LW7cnoDFCMk?si=uYg48Hx7QouD2H8rjYnEzw',
                'https://open.spotify.com/track/2ASMRdulqfuFhYAIw1dOUM?si=vpuMPsiPTFWEj_7F5lKPUQ',
                'https://open.spotify.com/track/5uFNJWnU1imR5jC5FuSLQM?si=jF9WdnePSIeR99E2GcQprQ',

                'https://open.spotify.com/track/42wOySSV3mE3lSo12wKbmL?si=i3ZhE515S7KYMzesfYYkvQ',
                'https://open.spotify.com/track/2PyAVQqdVKGYr6ZFuODNLJ?si=ARkYiC5YRIOTnHEtaHe7ww',
                'https://open.spotify.com/track/4XzCEurXfdtL3mj4dU6le0?si=6Kqrc4QlRWOfdwzH0egLtQ',
                'https://open.spotify.com/track/2MYPFXScWdR3PQihBQxu7x?context=spotify%3Aplaylist%3A37i9dQZF1DWZtZ8vUCzche&si=MsAm0sLXT4qtkivgJjHixA',
                'https://open.spotify.com/track/0tZkVZ9DeAa0MNK2gY5NtV?si=vkIK3AcuS-6cjOyKOlzPVA',
                'https://open.spotify.com/track/26pC4BgyjdRIeieIcGqLcw?si=TktI_BbUSOGjriXU0aAAYg',
                'https://open.spotify.com/track/1ZZNQEptyOyGbJA9RU3Uvr?si=D0CWHAQCQsW5CmJqTeur6A',
                'https://open.spotify.com/track/6c05B0BTOJbDyRy5KLI7my?si=o7AeaagPTvufy2lVZS3CRw',
                'https://open.spotify.com/track/26eURhEKaQ7pKLtGW0jyF5?si=FdZ9ayAjTB6Sp_BRLe_pHg',
                'https://open.spotify.com/track/01Zc2d1GLQ3SligNHtWeZr?si=G7NNf62iQ5uSrlQ6ReNL-g',

                'https://open.spotify.com/track/3wSEuaaOZe8LBV35uRBwIo?si=njrJRqQ7SAKhZFqzJBseqw',
                'https://open.spotify.com/track/1ZZNQEptyOyGbJA9RU3Uvr?si=kl63aQ2BRhGxswSYeFQBaA',
                'https://open.spotify.com/track/3Q4arvJHKco7FdQTsdpC6e?si=GmCAUScqSgOVB5Xsy7JUgg',
                'https://open.spotify.com/track/14f9BDKT2pvvSP5oK8qws3?si=XJqMifVeRTqD6mQ8pooBlg',
                'https://open.spotify.com/track/22fOsxYglRTjZcTOG8859P?si=NdFqIPewROOkaFQcORPu8w',
                'https://open.spotify.com/track/5PZYdz5eRfEPXrRyJgNKzX?si=Le5xKvdYSy2nRj5YFa0JvA',
                'https://open.spotify.com/track/2FygRDP2PuxcvWGGyf3nao?si=Xktrr8eFRiqN8q20jRiO1w',
                'https://open.spotify.com/track/5tRb0Y2bloJGI8uskuAtRL?si=ZH6xsR_cTnC1Bd9oOqpAaQ',
                'https://open.spotify.com/track/1FPat9MxjcvQNvhuVuBcmQ?si=94fz9hekQ6y8d5UKDN-ACQ',
                'https://open.spotify.com/track/1OzY7RRZh3EcIKn7VKZUTx?si=GveT2lx_TDuyWvsy1xPjCA',
                'https://open.spotify.com/track/4A5FLaZI3Ni5eT0c9fqi8F?si=HpI991oXTwqUpKU_sde_zw',
                'https://open.spotify.com/track/5lwwvBCUABdNcrIVYn6E15?si=PEjLMsNUTYar9rgcqIPyGw',
                'https://open.spotify.com/track/6XmdsD2GKYGMiAqqrM0WON?si=z-a41oirRaOct6PRxKN7Bg',
                'https://open.spotify.com/track/0q6LuUqGLUiCPP1cbdwFs3?si=c5gsJf2aTke1LbaNMwv42A',
                'https://open.spotify.com/track/3pLTOP0G0etiWUknFoRpsr?si=Iev-qRERT5ibkKi3_v9MYQ',
                'https://open.spotify.com/track/5KdhT7gtGHgE9uDKTppndY?si=ICNYCpBUR-SlR-MPC4NvNw',
                'https://open.spotify.com/track/70l2FSI4z3iUnP7vDnG1Us?si=bQehlR67QkugAwCphPJQgg',
                'https://open.spotify.com/track/7g3htkaLz4ETFn0cifwM3y?si=1OUwRfg2QbeV4fL-7m1z3g',
                'https://open.spotify.com/track/5OuJTtNve7FxUX82eEBupN?si=Qvr8NJyQTaWHmNfyID_w6w',
                'https://open.spotify.com/track/3B2cAYYUivsSuFGkFhnIGW?si=tmvKdtYITmSXsk3q5iJwWg',
                'https://open.spotify.com/track/3YB9cvd668HXBEq8rbBW8P?si=8RYSR8nYSJ2kiwBpDQc-zA',
                'https://open.spotify.com/track/4M5fqxO2LsqKA4AJqpduxv?si=MZmnvO6jSCqt0ogFCX0zXg',




                'https://open.spotify.com/track/2cNjgoSh1TBHFQIhfzRJUE?si=lmNm-UKuTuOlAsiRw_xpFQ',
                'https://open.spotify.com/track/1j0hMeC5fcnpwcsr3mH0pL?si=jN_yyPUhQkeJrFsOzvEwkA',
                'https://open.spotify.com/track/7HcvxFfcST0Jhu2uQ2JVE9?si=vJ3VM4QaTaisFzxFuyAvAg',
                'https://open.spotify.com/track/2Atzk0W2RHeZw2oIiaBubK?si=NyDLjIuMSGO50--7tSnzmw',
                'https://open.spotify.com/track/6ZzItbgnMdQ0cKFy4lFV7A?si=5J6ewzn3TCCiXBC1CutOig',
                'https://open.spotify.com/track/2tjWCe2W7sgvS3C8NHcdtI?si=L2i35HEaRn2M6fdl3dFnWw',
                'https://open.spotify.com/track/7zSrC8toa3hFPDD172Iyhj?si=Wp2M6EIoR1uCKrA69Vw7DQ',
                'https://open.spotify.com/track/62oJ45v2kAvi0mZZc5gR7c?si=r2tJ8mhiTiesupI2QceB2w',
                'https://open.spotify.com/track/282QGCfat8aMJ55RFV0BMb?si=MUubBAuMSeaypQFq2YdPbw',
                'https://open.spotify.com/track/5MC5l2JR9XN2a8Gjt7qMQK?si=QhSDQiHuQ5WoAskbna-0TQ',
                'https://open.spotify.com/track/0Zn63G0XTiqXwr1KSmARWz?si=VnQm56g7RQ2CBvOKSDrKSw',
                'https://open.spotify.com/track/5YHMaDiaGGYs5QyJ2CBDXJ?si=RwifaigUS0yTXl4PJT1jmw',
                'https://open.spotify.com/track/5fEVjw0eaCWgr3x1qpX7Oe?si=R9YR_8YWQY-j3IdpHkQKzA',
                'https://open.spotify.com/track/0ghfUnJYHNM4IVO8FSS5ht?si=fr24bvaKRQ6vw0XCLQhuGg',
                'https://open.spotify.com/track/3Jai674s9zQJJxsgsyRBHz?si=qYnRDv2AR1Orky5s29wNUg',
                'https://open.spotify.com/track/6oqAINdWzHols0AmwOTjeZ?si=VI_ZduLyRtOMAM4PB4_8Hw&context=spotify%3Auser%3Aspotify%3Aplaylist%3A37i9dQZF1DWWQRwui0ExPn',
                'https://open.spotify.com/track/4ApmPo6H0bH7PExQV25LDh?si=hXZClvCoRjqbFWu1EuO_SQ&context=spotify%3Auser%3Aspotify%3Aplaylist%3A37i9dQZF1DWSRc3WJklgBs',
                'https://open.spotify.com/track/1HwpWwa6bnqqRhK8agG4RS?si=tpL9ca5hRPiuqXn0cdEd1Q',
                'https://open.spotify.com/track/0zUJbZFIR5v2gCfbdg8yTS?si=BSRjxoAxQzOrYJroD07sqg',
                'https://open.spotify.com/track/7nEZZ1mWK7h98x8ENbQuqJ?si=CfM2R89tQCe6EtRmUu40gw',
                'https://open.spotify.com/track/64lsIF5pw0sJY0gV5kz0RN?si=_LNri8JBRVqXbFyKbh4NTA',
                'https://open.spotify.com/track/2wiKykLA8kPLZw7185qtTP?si=YSb4UT-BSFGYRDo1OCpS8g',
                'https://open.spotify.com/track/2mlGPkAx4kwF8Df0GlScsC?si=JhJt7iz0TTGdtNKIgwGrZw',
                'https://open.spotify.com/track/5C4QVrg1xnTqqJAON5VbAi?si=ZjW2KxA0TTCzBo-8JePtjw',
                'https://open.spotify.com/track/5rzIpXcH1ZmQ3owzAqd9vK?si=GqmaVk52RZ63yUG0RmnWvQ',
                'https://open.spotify.com/track/6cmPjiylmkjv2wiBCx2AHz?si=sDbowv72TRKkY58LdsDp2w',
                'https://open.spotify.com/track/5WXezeBcPemshsXjMCyi9b?si=8r8af0zXRO6-qw1HFwpd8w',
                'https://open.spotify.com/track/6ykYjWGPaFi9tWeQWkvVIE?si=OJtu2ypQR5yI5ex608Nn5A',
                'https://open.spotify.com/track/73VpGHucDuzwtFJiT59bEG?si=b_NP8f7nT-GVEl-ApNRsLQ',
                'https://open.spotify.com/track/4EfHV88Vix7C5iKNDUBEQc?si=1D7uK9PTRAKUuU-MLHEZrQ',
                'https://open.spotify.com/track/3WBsWNtL054HCFz7UUGK9e?si=e-cveTWsT0iGqqUUcKm-jA',
                'https://open.spotify.com/track/4TH3jYF0EoIIcwssYWJWeS?si=emajR8uGTZaS6kVNQPCISQ',
                'https://open.spotify.com/track/6cmPjiylmkjv2wiBCx2AHz?si=VDUk45sORw-BrfHCMsdVSw',
                'https://open.spotify.com/track/2Bc4llhjJBW77I552RgA3L?si=-80TXxugRzW0mtL9Prr1Sw',
                'https://open.spotify.com/track/6GMaQmdpwGolGyuW6ZJ9X9?si=TGEON65DRAKv297xUywOGg',
                'https://open.spotify.com/track/6crBy2sODw2HS53xquM6us?si=hZGM3uZ2SxqvRwZPflKU2g',
                'https://open.spotify.com/track/32zh7SvLPVVLJJ4MPuoVxM?si=IKjf0H9jRg-zNKemCVB39w',
                'https://open.spotify.com/track/3TFOpb4NV8Rt78OX4eyhE8?si=TAmoX2vLS7Cm8MZGR1WXXA',
                'https://open.spotify.com/track/6VU6nJ40P2Y2nuceLxTOto?si=38cueT5tST20dDk0jrHvmw',
                'https://open.spotify.com/track/4wiIuwsuopxoTRTu0GnuAN?si=mFzzQGwFRxmJnSwwLr7dGg',
                'https://open.spotify.com/track/4p1mnjogg0ZZ5O8ga1jD5C?si=iiAsek7JRCaCWpRKtKtmZg',
                'https://open.spotify.com/track/3auLvYd6YRgb1lTCp5FsIi?si=HJUmEH5dShe2aeE6K_NP0A',



                'https://open.spotify.com/track/6UGlSlhwl2MNhsrg5Wepq3?si=Hp4yX_TqSBaV983ymwpSQA',
                'https://open.spotify.com/track/69xUkf647IyVn8cJtQ4zRk?si=f6m_cxaKQYCChYLPWDvtpA',
                'https://open.spotify.com/track/1MIwRUsj23h7cYn6mNiqHw?si=JL-EIrKtT-G3gfcIUZqFlA',
                'https://open.spotify.com/track/0E1RvIsqe7cFPIkbM0PVEd?si=drrY-N_vSdWYZWLhd8PX6g',
                'https://open.spotify.com/track/4cZnC4CQacU7i1W6ko3Va2?si=ylQlbe_PRp2aUw5NmIk2-Q',
                'https://open.spotify.com/track/6W4pRJhZhyO3rz9vTITKRB?si=E_tPcLhWSMiv7o4kzieqOg',
                'https://open.spotify.com/track/0yc6Gst2xkRu0eMLeRMGCX?si=Gpq3q3b1T8eEyJ96flh_hg',
                'https://open.spotify.com/track/285ieonEuLkll3zknYK2TY?si=BXxehxbdTs6XTrnLfil6_g',
                'https://open.spotify.com/track/2pUfIeF044S7DQNdaOEAoR?si=xsVEpm09Rk6sT0q2tSGSQw',
                'https://open.spotify.com/track/3joCfQaNHoW7xrh7dImwiN?si=SYJRhV4gSYyRb4tWSK11Mg',
                'https://open.spotify.com/track/1uWNzsH146RBPoq7QNYw4c?si=79Z2mL-lTjGv8sDoHqjdRA',
                'https://open.spotify.com/track/73jVPicY2G9YHmzgjk69ae?si=TL_lrYiIRquBjJCy7t8BwQ',
                'https://open.spotify.com/track/5IR7Ui6MB7MrFZfF5hsoIH?si=Gz-4BJQrTA-lzljdj-3rMw',
                'https://open.spotify.com/track/7wCND5ZKuJbbBYZVKfUE4y?si=yK304NnzRn2D1L3AADykAg',
                'https://open.spotify.com/track/4e3d7O2rpHNwbPaMtqiy8o?si=23Mn7lnRRiCkBylw84BPSQ',
                'https://open.spotify.com/track/4HThk0Cu6yMGNNwvCt0NAk?si=n7XKZwJEQROaOtIQNcGZxA',
                'https://open.spotify.com/track/5Sl1RVQbD9PigheYMG7yAP?si=EaqNTQ2JT-yl78zKo3Xf1Q',
                'https://open.spotify.com/track/4vHNeBWDQpVCmGbaccrRzi?si=9N8ascoMQM2oFIVkxmn37Q',
                'https://open.spotify.com/track/70nmZhHZLNVYWP4NON41Zw?si=gGKvS9uUSWSf_GNBjwhM-g',
                'https://open.spotify.com/track/2djY65hifu2a4R2WqcXqKL?si=W89zmSrnReC7ModXfXNM-g',
                'https://open.spotify.com/track/14TEjsiW5PdgWDa2uncjQB?si=a4uwcjkSSHu0-V9nq14J3g',
                'https://open.spotify.com/track/7bre6yd84LZ6MFoTppmHja?si=rf2kkensRaWvBlp2kBaZ7A',
                'https://open.spotify.com/track/5rzIpXcH1ZmQ3owzAqd9vK?si=nKF07dxwRY6Hc3FS14nQUA',
                'https://open.spotify.com/track/6AFYnnMXGoZ6XklPfWEIu9?si=zwUb9LPGRTqQmz59Ma586w',
                'https://open.spotify.com/track/4z2JaAVPemYJhFKm7e32RA?si=-VV5Br2-Sy-xZ1vZGCNueA',
                'https://open.spotify.com/track/6soi0mNwTsygfHVdFrFYvH?si=Uf6CB05MRiOP-qwp1nK7tA',
                'https://open.spotify.com/track/0nbXyq5TXYPCO7pr3N8S4I?si=Es2MzlvPSq-ynwhSoMb9MQ',
                'https://open.spotify.com/track/1UWhx0pFZccP4jdCIZsj7U?si=CCC7Gm5XTTKUd2Dkm0g7vQ&context=spotify%3Auser%3Aspotify%3Aplaylist%3A37i9dQZF1DWSDznyru3cEZ',
                'https://open.spotify.com/track/3RtDQEXpu3VDgLB9DIGNFW?si=eWoLYFCmRL-ncXlCepYATA',
                'https://open.spotify.com/episode/2Ohw02THaMjuszMVhiD9gE?si=ZneDOq84Rp-WFGKrktMggg',
                'https://open.spotify.com/episode/38s9P4QGw5vwOMRrlupOHH?si=2Ux8B4f-Tuugk34GIb9TSw',
                'https://open.spotify.com/track/0cTkX0seXUBfZOrdxhecRh?si=zaq4j7PcQaiAZtmCH1svHQ',
                'https://open.spotify.com/track/289tqoUU4BsRFI2Zuf4FDT?si=nGabOwrJRviRnBSb_ZA87w',
                'https://open.spotify.com/track/3mfn2O8KHI7IW2lHemMSmA?si=oquIWQ9nSqicbFjXQFjRhg',
                'https://open.spotify.com/track/2DJDgwpCTrBHQUJUWPTjmo?si=P5VA3YywQ2-NDA7W6m7VcQ',
                'https://open.spotify.com/track/56Z3lLPTcozYkoAl9HsQLI?si=sBryzSUJR929oURkFJ0ZHw',
                'https://open.spotify.com/track/4NBYp73qsxFh9yUUnMy6jz?si=ybypmTJqRpSDE_sTte1aCg',
                'https://open.spotify.com/track/07iVScUe08QYNdEvjsEEGc?si=oDxib6zgTViPoQDXsmvYqw',
                'https://open.spotify.com/track/7DRomdqDAEVzcdeVwWb8Lj?si=wEpqFf1xRAOzkQuc3ZnQ3w',
                'https://open.spotify.com/track/3CSJynywxiscyFHJBJPJfT?si=GzUBkKOeQCGQxrVBe0eP1w',
                'https://open.spotify.com/track/7eJMfftS33KTjuF7lTsMCx?si=Xj2EoeLxTfacQPb5HNfaxw',
                'https://open.spotify.com/track/3dGrpNNzlT2iD89KK3cQT2?si=YM6u0R67Qr61UcsYapW5ww',
                'https://open.spotify.com/track/5m4X2HQ0eiviwuKPoREanT?si=lS85YKezRMOR4iAMh-RC9g',
                'https://open.spotify.com/track/4bndkI1TTh7itdsyixtDoD?si=GNfcc2HsSbSIAeE8X4_YrQ',
                'https://open.spotify.com/track/6nwRC0UkS1MdOOMjcJsrbX?si=GNIqVSX3QHCni7D_c4P-vQ',
                'https://open.spotify.com/track/62aP9fBQKYKxi7PDXwcUAS?si=ccLS5HkET2qQqOwwMtZsWg',
                'https://open.spotify.com/track/3YB9cvd668HXBEq8rbBW8P?si=ZfjJJmwYR9W_dsKzDYzPCQ',
                'https://open.spotify.com/track/285pBltuF7vW8TeWk8hdRR?si=aNykR51bQru5ccj3-Xlq5g',
                'https://open.spotify.com/track/7MiZjKawmXTsTNePyTfPyL?si=MgIHkZL1TGqalDDYdbQfGA',
                'https://open.spotify.com/track/568nXF19QXYPZnQ6XSkuSH?si=s1prQF2hSMaLn5Z_oA6prQ',
                'https://open.spotify.com/track/48PGeEeCqI5QZlUS9x4X6u?si=uFFymsf0SO2EORN_KOh3lA',
                'https://open.spotify.com/track/3n1EOQHgfxhmnsuhJM6Ro0?si=8y5CyoW4QZi-dwHLf2Olyw',
                'https://open.spotify.com/track/4ygSSIuPuM0EYu22s8YF4t?si=Y5xKrXvQQyy7JyzT-my_wA',
                'https://open.spotify.com/track/6RyY8r3DerLiB0hcBoTNFn?si=ItpT8oZKSr-S6V1mDLuEsQ',
                'https://open.spotify.com/track/2pSEhuPVhatz18cCLs5ZjY?si=f8bUFAuCRsG_hYL27XgjUQ',
                'https://open.spotify.com/track/1Jjd6QstbIZb6pa3GXmYl4?si=-lzhBpZJQI2HMKON794F-Q',
                'https://open.spotify.com/track/72IE105nTdzIkt4Dm2AFUq?si=vjHAXaY2QImqyZzgDQce5g&context=spotify%3Aplaylist%3A37i9dQZF1DX1HoONJoJCjL',
                'https://open.spotify.com/track/5poTkPZvxROL3RtuxRVtBU?si=OHQ4Tsf-Rnq5i_77sv9VLA',
                'https://open.spotify.com/track/4wSmqFg31t6LsQWtzYAJob?si=DlJBYVKDS4yiR3QscLWehw',



                'https://open.spotify.com/track/3lIxtCaROdRDuTnNBDm3n2?si=AWwqj5QjS3iN9FE--PKRCQ',
                'https://open.spotify.com/track/1ujxjsoNvh4XgS2fUNwkZ2?si=y1Nme0G_R7i4mT1r3mp5fA',


                'https://open.spotify.com/track/1BLOVHYYlH4JUHQGcpt75R?si=7-YHN47ZQru-ut0wmofLeA',
                'https://open.spotify.com/track/3VmCG4XZKfmqWayAXaL7pl?si=BcvG1GNeTBO6I6oVKH1CSQ',
                'https://open.spotify.com/track/4spKPzrQHxAZC59YpRxeNJ?si=Hr_kmHn1TCCe4Nx2Zyp6-g',

                'https://open.spotify.com/track/556jf0hyPQuLNHuNWo12I5?si=8aitj9HkQ2CRn0KjHHM6qg',
                'https://open.spotify.com/track/5drwkeWY5C8e2I6cTg79NS?si=ZQlFcMO6TI2CCv619brzwg',
                'https://open.spotify.com/track/3qrEG6rQ9Qm72MNWeUKKiU?si=1t029rkQSFmcoSiVb7ZCOw',
                'https://open.spotify.com/track/5wuMgzTz4CEypdWabWjkLp?si=JsM5-hZdRVGhCSoX1GqkCw',
                'https://open.spotify.com/track/3aK3iIvgT5FQgKAjLunrMN?si=iPTqT_YYQVezJI2wHOAB6A',
                'https://open.spotify.com/track/5I8uodnsRbVbBfGGj3rHnl?si=6dzptwOzSP6kW2W7RECtyA',
                'https://open.spotify.com/track/3c5Og78p3plOCBbNLg5K9L?si=nla4-u49SfueC_y-pk-wCQ',
                'https://open.spotify.com/track/5XeIQO9gGkGo54naYVVeJP?si=MTB1WbOORfWzzzoUBp1ENA',
                'https://open.spotify.com/track/3tIdsxOHer7VOMSwxAzw4T?si=yN2hqcgBQreP2EkaKkCS7Q',
                'https://open.spotify.com/track/6V97NdhQVsU4SwkUucepS3?si=p4scFrC5SIe7o5FGgGMb7Q',
                'https://open.spotify.com/track/69L4d5HlE0YOCwWFYVFGoW?si=fC55-pelQYyWAvbjXgX-sg',
                'https://open.spotify.com/track/2IsBpMTE5ht4vsPGEFD5Fc?si=Ih8nPGU-TfiO0O0BDtpE1w',
                'https://open.spotify.com/track/1XrSjpNe49IiygZfzb74pk?si=UdsEdHRyTIadPLPwQYXPRA',
                'https://open.spotify.com/track/7CQb2wqEbsx10Xuiv8LLXb?si=wM-okameRZKigpl-GfR7VA',
                'https://open.spotify.com/track/4MQ9Wg4zOELBEAldiZTzau?si=GKq4ch3qQF6glp9c-EUwKA',
                'https://open.spotify.com/track/1cZtKcNA9wmXRprvhKEdxm?si=J7_eH2qDSByTC2ppCuwi3A',
                'https://open.spotify.com/track/7t3MhCZgD0ISk0aJmw954y?si=0L7Wifb0T7yWRIEHcdyNTg',
                'https://open.spotify.com/track/0buXDUrVu4lRhFJ2lXOwKZ?si=kswijeOsTbC9CFdj3wMg4A',
                'https://open.spotify.com/track/2NDZ6i6UfOUSKgFiTQKbnv?si=xiQKomUURo6eU6ZYOueXIQ',
                'https://open.spotify.com/track/6rIThCnWLgi48NqcFLCedp?si=UxOG9pUTRJu3GAuGlpXIFA&context=spotify%3Aplaylist%3A37i9dQZF1DX1HoONJoJCjL',
                'https://open.spotify.com/track/3dJXvBddoH1AGLpKvmbYDA?si=JMzstR5BQUWwuYeKozpKvg',
                'https://open.spotify.com/track/6V97NdhQVsU4SwkUucepS3?si=LNd75NaXT3i2_G7AiyZrnA',
                'https://open.spotify.com/track/6eHkModpBlDnq8vsJ6Ndag?si=ebJx6RpdSsuw7mKv1c2X2g',
                'https://open.spotify.com/track/4TNm9fA5OIE8SDCBzX79it?si=ioOxlYTASxazWbXynQ0OYQ',
                'https://open.spotify.com/track/6simvKne22uVh5ryufUF8U?si=FiBVMxJ2SYqTv5Vkkg0Uig',
                'https://open.spotify.com/track/4fbvXwMTXPWaFyaMWUm9CR?si=vX5X8yFJQBii3K4Uj4eD9Q',
                'https://open.spotify.com/track/29idXL5KF3RhwAR6XIxt1y?si=rDiMXVOfTh2Oa5VJaG6wfg',
                'https://open.spotify.com/track/2S1LebN6AXXQqJolBxlWgO?si=iMGdGRsgQLedOH9y1t7y4g',
                'https://open.spotify.com/track/5XZK1CC3LybEKGdmH04YBC?si=pLpADoxgSKqqOYZw54Z6xQ',
                'https://open.spotify.com/track/11VwZwNF29HrqwalYUMitb?si=kr1Oyf6wR_2KuMRbXzwRxw',
                'https://open.spotify.com/track/6cA3HSqfxfGCYs3kmB5TrS?si=JAhMT5ZqSzyEZQ1cCqa4lA',
                'https://open.spotify.com/track/52Fw0bPlDegUpoETTxtIgf?si=ulm6JJMVQ-yjLV5UBzwl5A',
                'https://open.spotify.com/track/4cjRiT6COzETZ3mWQXydnr?si=eE5UjmknQvubiGkXG-JfDw',
                'https://open.spotify.com/track/5ZESanTyKmIOXBu7se7z6U?si=8bs-X-UXQIOfDQCl8FI1fg',
                'https://open.spotify.com/track/14qPNe9WNrBJFeweWlkUgU?si=mU-J9Da9QH-uG8lB1iY0Iw',
                'https://open.spotify.com/track/3U52igpu9mo4TGZdmRbZOy?si=Ef4y1ekJRNqHwIWaLscYuw',
                'https://open.spotify.com/track/1cl1Wckhfp6MtydmHjVOyd?si=98GLQU7nS_uqRSGcYPbD8g',
                'https://open.spotify.com/track/3BOtIwkhaJpTB9meCGEXUG?si=ImTcRBQ_SNmPo3u3J63VGw',
                'https://open.spotify.com/track/4CeBKWWLXMrQMFsP0Q0K3V?si=hdg05wAKRiKcZolZC_QKIQ',
                'https://open.spotify.com/track/6N5TNlYhmpuynRBlyXScV4?si=SzdJRmHES5SMXeiNEOXlfA&utm_source=whatsapp',
                'https://open.spotify.com/track/4VCKj1eGRZ0snkb5WLgLsX?si=DgGC_PLWR-aXbJ92zf28gg',
                'https://open.spotify.com/track/3DNRdudZ2SstnDCVKFdXxG?si=aYx9Egj-QEy0nwlPruKpQw',
                'https://open.spotify.com/track/4lhUziuDKvQJu7ZW9cLmIv?si=JCFxSGWETJyNRtHoM7LYcw',
                'https://open.spotify.com/track/4VCKj1eGRZ0snkb5WLgLsX?si=kVkd8pbuQaazS3Cfo7Nneg',


                'https://open.spotify.com/track/7zXMexKnhAYV6biVbHwF0o?si=H87HHz1eRnK3vvyuAFBOqQ',
                'https://open.spotify.com/track/6UqRGwjwYL0stXbaodTxwo?si=V7NxJhInT7iQtiZt9ys45A',
                'https://open.spotify.com/track/76IijT19KtStPt9ij4nNk5?si=t61-_xglSGmrZ41JRvCXxQ&utm_source=whatsapp',
                'https://open.spotify.com/track/5MXSLWGyPosYJ09LNu12SO?si=kxshC-9NQPyudEUtyxC_eg&utm_source=whatsapp',
                'https://open.spotify.com/track/69Yia3qCLw6N9U80WhLwLn?si=xY35KQPgSqu4KZQDnibyvA',
                'https://open.spotify.com/track/6ypqzijMjsopQkfMLrImQp?si=7B7lKfutSc67pvLA-QAq7w',
                'https://open.spotify.com/track/3V80b6XYyAc2vD9s7tddxG?si=2HhI8wcaSGyXZsyahT6B6A',
                'https://open.spotify.com/track/1MJ5f5EYBC92ADD6xcz7nb?si=l-agzBJ3R4iNyhnP0zXRSQ',
                'https://open.spotify.com/track/438xBTovrKS6vp9mWqvtSE?si=HPS6hRDzSDmyM9LD4yH9jg',
                'https://open.spotify.com/track/53XM8O6sQ4YzCq2jYgXuC6?si=ccGjqzMuQG62k9c_5vKFiQ',

                'https://open.spotify.com/track/6Ln89sczgIcAJXGAIdS94R?si=e6rhhKl5RXaxcXuE7JAtlQ',
                'https://open.spotify.com/track/2bb6xgxu1sevom4tn6OBSq?si=5ejErCGQSpq2qjvjbjgd4g',
                'https://open.spotify.com/track/0D9yiSJ2f93D44a2Wk9yXS?si=V8-up-7TTR6rw2Cch_5pKQ',
                'https://open.spotify.com/track/79hEgvfXVNbYT2AjaJ7ake?si=2-khUDx3Sci46pJKDLC9_Q',
                'https://open.spotify.com/track/5hlMwqtOhJVwX0ih39qwSf?si=N1vuINhzRHizef0Oix-Zug',
                'https://open.spotify.com/track/10glJ8ARN1G9ESFF9s00yk?si=UNvSFmlJQRW8tSNn8m46rg',
                'https://open.spotify.com/track/0YXCJlidjXsr7vnu7EXZtH?si=VkpJ3PAvQW64cEbamxk42w',
                'https://open.spotify.com/track/7vuwfilgaYreKxeyzQZTJf?si=R90DYV9FQ96DXF_7ZaVBqg',
                'https://open.spotify.com/track/0DMzkDvrWz7GaTNf3257uZ?si=uVCKoQAaSueHoRH18r-k_w',

                'https://open.spotify.com/track/2Atzk0W2RHeZw2oIiaBubK?si=5udwd4_JTQu-ckVDOHTBtQ',
                'https://open.spotify.com/track/5MZ3ZUvMFbS0zKis6DwmAM?si=6bytyWejTbaKH3LkqrGH6w',

                'https://open.spotify.com/track/4ose2wGsEKEajs2TGpe1eD?si=5Oy3XNgHSvaG3PyyrBV9lQ',
                'https://open.spotify.com/track/37WBfdm7B3blOtJMxDyc5g?si=NhdeEUvCQBGWc5SGr0jfnA',
                'https://open.spotify.com/track/5G3ZKjCHie2Ikr3I4QCQGt?si=6wXdbavMTmyh98RgB8woDg',
                'https://open.spotify.com/track/1cxegHCKLxQrcxsBzXmWpB?si=tQUO4k8cSV6QBRlo9EX08w',
                'https://open.spotify.com/track/0s8AZmbg5DnkjaYRCEWDpM?si=1cuCJI3OTt2CDwF1uhvXWQ',
                'https://open.spotify.com/track/3knkVBvRx1k2au2ZnywrPt?si=R-CtIB5wR5OrgPM5LgoCrQ',
                'https://open.spotify.com/track/4VCKj1eGRZ0snkb5WLgLsX?si=_WGzFuVZQGueqTbXlrt04w',
                'https://open.spotify.com/track/3s7MCdXyWmwjdcWh7GWXas?si=Yc1s3nrSS1yu672-OfwB6Q',
                'https://open.spotify.com/track/3Va1RWkIfhCEdo1MHVerfR?si=KSfxtr4sS1qZOTzrTtcrIQ',
                'https://open.spotify.com/track/4oxOGrHTfkfFIlJVvlcfpq?si=hj8hCmZBR5SQyIq7Ax1c1Q',

                'https://open.spotify.com/track/1bQJHs55iJ5DDPR1MjPQzG?si=csJbAoe1TcqA8-OdW-g2vw',
                'https://open.spotify.com/track/5HpQ2SuB4EWkEvUhNYh75t?si=t2WpEeGaTJCQIjLfXjx_ww',
                'https://open.spotify.com/track/4wiIuwsuopxoTRTu0GnuAN?si=5pb1ZSM8RiK307SG4VAwqw',


                'https://open.spotify.com/track/3DICPaa3WhXrwqiooSWOSB?si=sfcZd-QgSYKQtbljIdLexQ',
                'https://open.spotify.com/track/6iU1wS1dJh61wMBnoy55Mu?si=dDSlSHS6TI2faePKxqPPgQ',
                'https://open.spotify.com/track/57DdS3F93lpn1h45nmXkGu?si=jP-Te6u9T0qV1xSAnXIHiA',
                'https://open.spotify.com/track/5HCrm5tm2Lrvc18TFt4dCJ?si=HQMZaWKVT8Kk9U4ojpmJzw',
                'https://open.spotify.com/track/7xPQY7skgsujvvVyoE5lBi?si=Q-YFYogbT3aUJzw-E5B8mw',
                'https://open.spotify.com/track/7eOJ0Fe4dJdpFE5KiDNv7A?si=DNN5hSY_QMOwmFDbjQHIZQ',
                'https://open.spotify.com/track/0fxGA5lxrdYNYoE7yJxTNZ?si=QmKU7cBrTjCNKYKqULxgDw',
                'https://open.spotify.com/track/2XmEDW2SUbYYt5o2cxSEz4?si=qaaHAZALT3eJc5thSl9csA',
                'https://open.spotify.com/track/0GyXfYRuvG9nt71zF99SER?si=m8tPCRuiRd-9Gs9gmZoj9A',
                'https://open.spotify.com/track/1rv46mRwDqMEhOBZ7vODg3?si=glJW7CaxTFKufmWdnl0Rvg',
                'https://open.spotify.com/track/11eWp7aUhs9RShuCrnglDc?si=QJhhbQiMT8GNcLdIkkcSgg',
                'https://open.spotify.com/track/43DeSV93pJPT4lCZaWZ6b1?si=uVT0G3WUTNuvMzRw0nd_ag',
                'https://open.spotify.com/track/0Psz3az3RIYfJpnsajBT8N?si=L7LAGmX1SHevalTLdMJMcg',
                'https://open.spotify.com/track/4oKQPfmBkN7UPuQVvqS5Np?si=hcP84V3iQmSZCsRrnbpLmA',
                'https://open.spotify.com/track/4TXVuIAvpDcrxw2DcOj3v3?si=rOfzm4fURZ6RBQnmn1v_Vw',
                'https://open.spotify.com/track/2vAhq1zwhOBcNvYchGXvjc?si=J4S6lD5oToqleow5D5I8jg',
                'https://open.spotify.com/track/02dPa4nXABwnFzjZosKxsk?si=4uKRr-_xQZ-QB2LJybH46A',
                'https://open.spotify.com/track/6vKTm5I3Nqpw6CJt7NgHLz?si=XIUEafjhQvKyFZFEqD9-EQ',
                'https://open.spotify.com/track/6Jfpv3vvfobay7uYVxWXog?si=aQZj0T1ZSM6qkzg0SnkS6g',

                'https://open.spotify.com/track/36vmjzpqqcH4zryJPlyHwP?si=bthDbk9KTIycvcVY-HXaXQ',
                'https://open.spotify.com/track/5bgOnX2KXKiC006R5hnHAJ?si=bM5Pc49dRP68YPcwkndTOw',
                'https://open.spotify.com/track/0ZnwzjB40zdTZrEwPvaRqG?si=s0_sXrXuQyqCkjog9bLhuQ&context=spotify%3Auser%3Aspotify%3Aplaylist%3A37i9dQZF1DXd9vfK9DV3I6',
                'https://open.spotify.com/track/6EiNPCNOmYBLJFy5kf68Va?si=bn-lGKjfTXetoPHdysEGaw&utm_source=whatsapp',
                'https://open.spotify.com/track/7xlrdBdz8TGSo0COvLHymc?si=eMhQUP8vSN6YMTTggGRuaA',
                'https://open.spotify.com/track/0IrPLnJlvxkOeO9PJSlIhr?si=5fVOjevFSyKhk1NBWDA9sw',
                'https://open.spotify.com/track/40wUM3LFZOlUcZfxEIZrYK?si=xVCLhJJwTQGN5hqywFwdcA',
                'https://open.spotify.com/track/4VvTumh88DI240WO9ej6OV?si=ZJ6SPqK6TFaYK7_Tw85qUg',
                'https://open.spotify.com/track/6H4WlsYhmoHR32cjoBEx8P?si=PFfI71bnSHqm0eHYUTVPzA&utm_source=whatsapp',
                'https://open.spotify.com/track/7dEYUkZMdUs7rfOKRMr5lO?si=nLaM1s7ESKGVwjHqGuSVKA',
                'https://open.spotify.com/track/6FLwmdmW77N1Pxb1aWsZmO?si=eA-35u0KREmtJ42lxaRLfA',
                'https://open.spotify.com/track/3m3TpmwZDF1UGC4v6Fwhfk?si=YOdclhiqRjqbszJyD1gjwA',
                'https://open.spotify.com/track/7nda0GK3uUnKgngFzNuYhx?si=takK6wpORci8IbVpxIF_Eg',
                'https://open.spotify.com/track/1Ot6UNRGj2aYS3xtqw1YtA?si=xbHwgtC2QsSbTZkqLNNyxw',
                'https://open.spotify.com/track/6V0cqtIK4V5e1z4waoohDd?si=pUoVffWoTG62frKmVZJaHA&utm_source=whatsapp',
                'https://open.spotify.com/track/49acDBy9eCghAkXVdqRusk?si=usTysmtWR0anjt7pE2VJOQ',
                'https://open.spotify.com/track/6Jfpv3vvfobay7uYVxWXog?si=dJsxDANsRfuqJLscQS7liQ&utm_source=whatsapp',
                'https://open.spotify.com/track/2WAHi5ZJwDZqGjnhZgZYmU?si=--RPKCpWSNiCsmZbcqPSBg',
                'https://open.spotify.com/track/3bbqxT5UGZsvTy1r3txs0t?si=5LSySSENRUOCKN_KwKJI0w',
                'https://open.spotify.com/track/0oN921mKYPOVYhKceZofrs?si=i2HPeV2HR9q4U3hfCoB_IQ',
                'https://open.spotify.com/track/73oamquev2r1MMkSDEjKgQ?si=PRRvPjmoR42N_q5aTjUhdw',
                'https://open.spotify.com/track/6oxemotUd24kJINSZgsEKS?si=efiS2a24QNKdM946YnQr_w&utm_source=whatsapp',
                'https://open.spotify.com/track/5F3t5WgLyBX2W7un8IXiLD?si=hdIqDB2dR8CG3sX2_0TCbg&utm_source=whatsapp',
                'https://open.spotify.com/track/4y8EK77j9dgfA4Ewig3Ad1?si=oe_WErJiTnS-uAaAourdXQ&utm_source=whatsapp yeah',
                'https://open.spotify.com/track/3m3TpmwZDF1UGC4v6Fwhfk?si=Zdyr3ARySJaOoSXDsf9HvA&utm_source=whatsapp',
                'https://open.spotify.com/track/3PDcJzbBq2rwBAwny82gJm?si=fy5M_wCCTVObvZAZ183cHw&utm_source=whatsapp',
                'https://open.spotify.com/track/0YDPNHKTSC0agSj7BJRkLA?si=8xIr8-W_RGmlFkLKLrk5Aw&utm_source=whatsapp',
                'https://open.spotify.com/track/6gb9RppaNsLof48ZTSYxhv?si=8paErTgWTY2A_qwCsfL5Mg&utm_source=whatsapp',
                'https://open.spotify.com/episode/4gxFQqDsqndyW8SokYJPE6?si=U5e4i-VKRK6fY79eC4_APg',
                'https://open.spotify.com/track/3Uwcyve5afWP54jgN0B5cy?si=u_OlIc2ORwqAidhp1P7Ozg&utm_source=whatsapp',
                'https://open.spotify.com/track/0saGACKtFP1ZVW4Nd4IkCw?si=b6as1Yy0S0m-gGcdlfJ8hA',
                'https://open.spotify.com/track/4qDHt2ClApBBzDAvhNGWFd?si=P4gY9AmiTAeY9Wf4Q4zR7w',
                'https://open.spotify.com/track/62p6fF2r4NY6pwZbxxvmr8?si=6kNPIhS0R-yAgZyGgRHIYg&context=spotify%3Aplaylist%3A37i9dQZF1DX8pxtTvJ2V4V',
                'https://open.spotify.com/track/2DCGf0V1FO3FR2TQXb7kAZ?si=grnqOMULQKS6M6K4ROFt5w&utm_source=whatsapp',
                'https://open.spotify.com/track/58f4twRnbZOOVUhMUpplJ4?si=pcjeP-CWSKyZsB4K29Aobg&utm_source=whatsapp',
                'https://open.spotify.com/track/1bVe7em86sIb8jW3SUZF0Z?si=lVe8HniPTVatSmyWUC-bfg&utm_source=whatsapp',
                'https://open.spotify.com/track/62IihiyUNMZ52oSnX55Bi4?si=soPGDnDaT_CzfXTSUBfU2g&utm_source=whatsapp',
                'https://open.spotify.com/track/3v3FEONiwvufayPNcWzHhc?si=eHP-anXKR46DmZ7LswwS0w&utm_source=whatsapp',
                'https://open.spotify.com/track/67hbP9PFQZrb4XZc3TzB0s?si=UJVl8XePROel3tKVnfyXTQ&utm_source=whatsapp',
                'https://open.spotify.com/track/4geScOJv4iQKceWrtXvASm?si=-T4bGPYDQly92qUagXCXKw',
                'https://open.spotify.com/track/4sKeiBIJi5gENURIMC3pW5?si=959bUr2yRF6r6r_MwHUlRw',
                'https://open.spotify.com/track/18V1UiYRvWYwn01CRDbbuR?si=hlNPnSLJS8S48ScqP3yRtA&utm_source=whatsapp',
                'https://open.spotify.com/track/3RkQ3UwOyPqpIiIvGVewuU?si=YmbfmNkuR5utTj38nBgLIw',
                'https://open.spotify.com/track/6QPhpvO1pWDS91EsEmzsbc?si=wtBt_tsfTDOTBtpiyzkbRg',
                'https://open.spotify.com/track/1v2zyAJrChw5JnfafSkwkJ?si=4HNy1dGMQ6mt8LbyyND6Ug',
                'https://open.spotify.com/track/1baHxgYktT8eDdmtTozJF9?si=STqZcMIlRjGVuC_NHGvc9Q',
                'https://open.spotify.com/track/4cjRiT6COzETZ3mWQXydnr?si=0ZBizUtGTEG0HRM00syTWA',
                'https://open.spotify.com/track/0hWzB4dR1zwcokPvccww0k?si=bN-3XoMJSv-zln_8EJ1MaA&utm_source=whatsapp',
                'https://open.spotify.com/track/5ql2mP9FUhB3SgMzv2akuO?si=tz41WoQuSlufJ4Vk0VJ5Cw&utm_source=whatsapp',
                'https://open.spotify.com/track/4jM545c2DEKT78TYRSSzIr?si=vdprffAmQrCAT_hHI5haLw&utm_source=whatsapp',
                'https://open.spotify.com/track/6YLcnMrPDdNSgvkie3yZ2U?si=NnPL0wNVStWW4p8rv98heA&utm_source=whatsapp',
                'https://open.spotify.com/track/6t1FIJlZWTQfIZhsGjaulM?si=u6UqKpJoRBa2FsQ4Lkd6Ow&utm_source=whatsapp',
                'https://open.spotify.com/track/26ky3sBMKv31Kpvil5pGDh?si=MaLI0y6nTIKARTZX6nXByg&utm_source=whatsapp',
                'https://open.spotify.com/track/1CRy08G60mS5jvhB27xMpS?si=Z7hVhPYzSvqe5XM5xSGsMg&utm_source=whatsapp',
                'https://open.spotify.com/track/5DRGuHS0xJ3X3OZjCrglTI?si=nTDdCh6XQCKVrt13lkhbfQ',
                'https://open.spotify.com/track/6KkyuDhrEhR5nJVKtv9mCf?si=xoRTQum3TUS6kqS-PORuhg&utm_source=whatsapp',
                'https://open.spotify.com/track/1v1oIWf2Xgh54kIWuKsDf6?si=rsA4CXIgStm7R0LJvpifAQ&utm_source=whatsapp',
                'https://open.spotify.com/track/3Jai674s9zQJJxsgsyRBHz?si=_EgT5kMbSaONFCZcJ6bGxQ&utm_source=whatsapp',
                'https://open.spotify.com/track/4U45aEWtQhrm8A5mxPaFZ7?si=3LBAosNsSDOgFw3ZzGkiqA',
                'https://open.spotify.com/track/2L7eiwosmluifpAVmrvVtm?si=0DU_fV_jRUiOTgkvuKe3FA',
                'https://open.spotify.com/track/2zQ2vKm9VslwOerYEWHtaF?si=cd4Rx19xRqu1wosBhzOZzQ',
                'https://open.spotify.com/track/3qsMWrhTbsiTQVykS3AeO5?si=93ZT-DifQkiR_NzaF15SdA',
                'https://open.spotify.com/track/74Dn2KLL8i6sAJoQh6hIRJ?si=AB9c5T-8QMChc810iOGo8w',
                'https://open.spotify.com/track/2bZNwQvu1GQn0DvytrSwUx?si=42xc7Pe9TIGyLtZnRG2zkA',
                'https://open.spotify.com/track/6Yn08sgGjRB2TARWyFqb70?si=UTWJqywoTR2g2ZTzCrimUw',
                'https://open.spotify.com/track/5CBG9UwXBAZqKg97xzOUVN?si=iFCHEA_9Tsu2FL6tCSSmEQ&utm_source=whatsapp',
                'https://open.spotify.com/track/3Jai674s9zQJJxsgsyRBHz?si=9uPkuNtdTLmGypMJG-EuBw&utm_source=whatsapp',
                'https://open.spotify.com/track/5HjBpej4uHPAX8sMeUFJms?si=klSnlFH6Sbu-4HMqpfbAZA&utm_source=whatsapp',
                'https://open.spotify.com/track/1cjYtL6yMFDLyZYn9bDkGo?si=0fWsUrDKRAqJpp5X47_XJQ&utm_source=whatsapp',
                'https://open.spotify.com/track/16qYlQ6koFxYVbiJbGHblz?si=Tp0LZMOcSC-ocitQQlJxng&utm_source=whatsapp',
                'https://open.spotify.com/track/3umugAkzQbdcOamNhjyIl7?si=P487XulRR6WyX5slgRQUmQ&utm_source=whatsapp',
                'https://open.spotify.com/track/4o7Rszx7VVCzrCr1RPlPot?si=YyqV_GFzTEqN70NNwI3_pg&utm_source=whatsapp',
                'https://open.spotify.com/track/59c7vs87nANrDrphf0gDBi?si=N1qNXBhcTyKo5iQUQK8w6Q&utm_source=whatsapp',
                'https://open.spotify.com/track/0PvFJmanyNQMseIFrU708S?si=ni4FHwNXRLquvvMdVUkVGA&utm_source=whatsapp',
                'https://open.spotify.com/track/7N3AWpme64LhM1P8I6yIZx?si=3Q-MtPrMQ2SdIN1GxR6rtQ&utm_source=whatsapp',
                'https://open.spotify.com/track/3PDcJzbBq2rwBAwny82gJm?si=Vmw-Z9S3SpWSFxC_TqIIKA&utm_source=whatsapp',
                'https://open.spotify.com/track/3m3TpmwZDF1UGC4v6Fwhfk?si=UT4TDL7iQsGdGVvQf1wiOQ&utm_source=whatsapp',

            ],
        ]
    }
}

parser = argparse.ArgumentParser(description="🎷 Sync your Spotify music with your MP3 player!")
parser.add_argument("-s", help="process playlist, download, and sync with target drive", action='store_true')
parser.add_argument("-ds", help="sync downloaded files with your target drive only", action='store_true')
# parser.add_argument("-r", help="loop the process after 2 hrs", action='store_true')
parser.add_argument("-v", help="get more output?", action='store_true')
parser.add_argument("-d", help="Developer use only, for debug", action='store_true')
args = parser.parse_args()

client_credentials_manager = SpotifyClientCredentials(configs['spotify']['client_id'],
                                                      configs['spotify']['client_secret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def p(print_string):
    """
    Print stuff ?
    :rtype: object
    """
    print(print_string)


def search_youtube(text_to_search):
    """
    Search the text on youtube and return its parsed results with title, channel name, desc and duration
    :rtype: object
    """
    query = urllib.parse.quote(text_to_search)
    url = "https://www.youtube.com/results?search_query=" + query

    try:
        response = urllib.request.urlopen(url)
        html = response.read()
        html = str(html, 'utf-8')
    except Exception as e:
        p('😥 Youtube gave up, this is so sad, can we get 1 like ' + repr(e))
        return []

    # find and get video id from html string.
    start_string = 'var ytInitialData = '
    end_string = ']};</script><script nonce='

    start_position = html.find(start_string)
    start_position += len(start_string)

    end_position = html.find(end_string)

    # get the youtube object
    object_string = html[start_position: end_position + 3]

    # trim the end and remove the last ; semi colon
    my_fav_object = object_string.strip()[0:-1]

    fav_object = json.loads(my_fav_object)

    list = \
        fav_object['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][
            0][
            'itemSectionRenderer']['contents']

    selected_video = False

    video_list = []
    for item in list:
        if 'videoRenderer' in item:
            videoId = item['videoRenderer']['videoId']
            title = item['videoRenderer']['title']['runs'][0]['text']
            time = item['videoRenderer']['lengthText']['simpleText']
            description = ''
            if 'descriptionSnippet' in item['videoRenderer']:
                description = item['videoRenderer']['descriptionSnippet']['runs'][0]['text']
            channel_name = item['videoRenderer']['ownerText']['runs'][0]['text']
            seconds = give_me_seconds(time)
            # selected_video = {
            #     'video_id': videoId,
            #     'title': title,
            #     'time': this_video_seconds,
            #     'description': description,
            #     'channel_name': channel_name
            # }
            video_list.append({
                'title': title,
                'channel': channel_name,
                'description': description,
                'href': '',
                'video_id': videoId,
                'duration': time,
                'duration_seconds': seconds
            })

    # page = BeautifulSoup(html, features='lxml')
    # vid_list = page.find_all('div', attrs={'class': 'yt-lockup-content'})
    #
    # for vid in vid_list:
    #
    #     title_link = vid.findChild('a', attrs={'class': 'yt-uix-tile-link'}, recursive=True)
    #     if title_link is None:
    #         continue
    #
    #     title = title_link.attrs['title']
    #     href = title_link.attrs['href']
    #
    #     duration_el = vid.findChild('span', attrs={'class': 'accessible-description'}, recursive=True)
    #     if duration_el is None:
    #         continue
    #
    #     duration = duration_el.text
    #
    #     channel_name = ''
    #     channel_name_el = vid.findChild('a', attrs={'class': 'yt-uix-sessionlink'}, recursive=True)
    #     if channel_name_el is None:
    #         channel_name = channel_name_el.text
    #
    #     video_description_el = vid.findChild('div', attrs={'class': 'yt-lockup-description'}, recursive=True)
    #     video_description = ''
    #     if video_description_el is not None:
    #         video_description = video_description_el.text
    #
    #     if duration.find('Duration') == -1:
    #         continue
    #
    #     duration_parsed = duration[duration.find(':') + 2:-1]
    #     # not parsing hour long stuff right now: example: 1:01:49
    #     # if the target video is more than 1 hr, consider it has 1 hr.
    #     if len(duration_parsed) > 5:
    #         duration_parsed = '59:59'
    #
    #     duration_in_seconds = int(duration_parsed[int(duration_parsed.find(':')) + 1:])
    #     duration_in_minutes = int(duration_parsed[:duration_parsed.find(':')])
    #     total_duration_in_seconds = duration_in_seconds + (duration_in_minutes * 60)
    #     video_id = href[href.find('?v=') + 3:]
    #     video_list.append({
    #         'title': title,
    #         'channel': channel_name,
    #         'description': video_description,
    #         'href': href,
    #         'video_id': video_id,
    #         'duration': duration_parsed,
    #         'duration_seconds': total_duration_in_seconds
    #     })

    return video_list


def give_me_seconds(time):
    time_array = time.split(':')
    time_array.reverse()
    # time_array.
    c = len(time_array) - 1
    seconds = 0
    while c >= 0:
        sec = int(time_array[c])
        c2 = c
        while (c2):
            sec *= 60
            c2 -= 1
        seconds += sec
        c -= 1

    return seconds


def download_video(video_id, file_name):
    """
    Download the audio format 251, and store it in file_name

    :rtype: object -> file name
    """
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
    """
    Convert the downloaded webm file to mp3
    :rtype: object
    """
    source = source.replace('/', '\\')
    target = target.replace('/', '\\')

    # fnull = open(os.devnull, 'w')
    # subprocess.call('.\\ffmpeg\\bin\\ffmpeg.exe -threads 6 -i "' + source + '" -vn -ab 128k -ar 44100 -y "' + target + '"', shell=True, stdout=fnull, stderr=subprocess.STDOUT)

    os.system(
        '".\\ffmpeg\\bin\\ffmpeg.exe -hide_banner -i "' + source + '" -vn -ab 160k -ar 44100 -y "' + target + '""')


def tag_mp3(file_path, track):
    """
    tag that mp3, insert artist, album, track names and album art.
    :rtype: object
    """
    f = eyed3.load(file_path)
    if f.tag is None:
        f.initTag()

    if track['album_art'] is not None:
        content = requests.get(track['album_art']).content
        f.tag.images.set(3, content, 'image/jpeg')

    f.tag.comments.set(track['search_term'] + ' = ' + track['selected_result'])
    f.tag.artist = track['artist']
    f.tag.album = track['album']
    f.tag.album_artist = track['artist']
    f.tag.title = track['name']
    f.tag.track_num = track['number']
    f.tag.save(None, (2, 3, 0))


def clean_string(filename):
    """
    Clean the string, only keep alnum, spaces and -
    :param filename:
    :return:
    """
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

            if 'user' not in playlist_info2:
                playlist_single_info = {
                    'name': 'songs',
                    'path': 'songs/',
                    'tracks': playlist_info2['song_ids'],
                    'playlist_id': False,
                    'type': 'spotify',
                    'user_id': False,
                    'user_name': False
                }
            else:
                try:
                    info = sp.user_playlist(playlist_info2['user'], playlist_info2['playlist_id']);
                except:
                    p("\n Failed to get playlist " + playlist_info2['playlist_id'])
                    os._exit(1)

                owner_name = info['owner']['display_name']
                p('Fetching playlist information for ✔ id:' + owner_name + ' playlist: ' + info['name'])
                path = clean_string(owner_name[:6] + '-' + info['name'])

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

        get_playlist(playlist_info)
        get_spotify_playlist_threads += 1
        # t = threading.Thread(target=get_playlist, args=(playlist_info,))
        # t.daemon = True
        # t.start()

    while get_spotify_playlist_threads != 0:
        time.sleep(.1)

    return get_spotify_playlist


def get_spotify_tracks_individualy(tracks2):
    trackIds = []
    trackGroups = []
    tracks = {'tracks': []}
    limit = 10
    p('')
    for t in tracks2:
        parts = t.split('?')[0].split('/')
        id = parts[len(parts) - 1]
        trackIds.append(id)
        if len(trackIds) == limit:
            trackGroups.append(trackIds)
            trackIds = []

    p('Made ' + str(len(trackGroups)) + ' track groups from tracks')
    for g in trackGroups:
        p('getting tracks for group')
        t3 = sp.tracks(g)['tracks']
        tracks['tracks'] = tracks['tracks'] + t3

    parsed_tracks = []
    for t in tracks['tracks']:
        if t is None or 'name' not in t:
            continue

        track_name = t['name']
        artist_name = t['artists'][0]['name']
        album_name = t['album']['name']
        path = clean_string(artist_name + '-' + track_name)

        def compose_term(term, lim):
            composed_terms = []
            index = 0
            for t in term.split(' '):
                if len(t) > 1:
                    if index <= lim:
                        composed_terms.append('"' + t + '"')  # make strict search for first 5 words
                        index += 1
                    else:
                        composed_terms.append('' + t + '')  # not so strict search for later words

            return ' '.join(composed_terms)

        composed_term = compose_term(clean_string(artist_name), 2) + ' ' + compose_term(clean_string(track_name), 4)
        search_term = composed_term + ' ' + configs['song_selection']['append_search_term']

        track = {
            'name': track_name,
            'search_term': search_term,
            'artist': artist_name,
            'album': album_name,
            'path': path + '.mp3',
            'number': t['track_number'],
            'id': t['id'],
            'duration': int(t['duration_ms']) / 1000,
            'disc_number': str(t['disc_number']),
            'artist_id': t['artists'][0]['id'],
            'release_date': t['album']['release_date'],
        }

        images = t['album']['images']
        if len(images) > 1:
            image = t['album']['images'][1]['url']
        elif len(images) == 1:
            image = t['album']['images'][0]['url']
        else:
            image = None

        track['album_art'] = image

        parsed_tracks.append(track)

    return parsed_tracks
    # sp.tracks()


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
        path = clean_string(artist_name + '-' + track_name)

        def compose_term(term, lim):
            composed_terms = []
            index = 0
            for t in term.split(' '):
                if len(t) > 1:
                    if index <= lim:
                        composed_terms.append('"' + t + '"')  # make strict search for first 5 words
                        index += 1
                    else:
                        composed_terms.append('' + t + '')  # not so strict search for later words

            return ' '.join(composed_terms)

        composed_term = compose_term(clean_string(artist_name), 2) + ' ' + compose_term(clean_string(track_name), 4)
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
        if not isinstance(pl, str):
            songIds = []
            # loop over the songs url list, and store ids
            configs['playlist']['spotify_parsed'].append({
                'type': 'songs_list',
                'song_ids': pl,
            })
        else:
            user = pl[pl.find('user:') + 5:pl.find('playlist:') - 1]
            pl_id = pl[pl.find('playlist:') + 9:]
            configs['playlist']['spotify_parsed'].append({
                'user': user,
                'playlist_id': pl_id,
                'type': 'playlist',
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
    p('pl:' + str(total_playlist_cd) + '/' + str(total_playlist) + '-tracks:' + str(total_tracks_cd) + '/' + str(
        total_tracks) + ' - ' + s)


def clean_temp():
    p('Cleaning temp')
    files = os.listdir('./')
    for f in files:
        if f.find('.webm') > -1:
            p('Removing temp file: ' + f)
            os.remove('./' + f)


process_playlist_threads = 0
parsed_playlist = []
hr = '───────────────────'


def process_playlist():
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
    songs_not_found_list = []
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
            if (pl2['user_id'] == False):
                tracks = get_spotify_tracks_individualy(pl2['tracks'])
            else:
                tracks = get_spotify_tracks(pl2['user_id'], pl2['playlist_id'])
            total_tracks += len(tracks)
            p('Got ' + str(len(tracks)) + ' tracks from ' + pl2['name'])
            pl2['tracks'] = tracks
            parsed_playlist.append(pl2)
            process_playlist_threads -= 1

        while process_playlist_threads > configs['concurrent_connections']:
            time.sleep(0.5)

        get_playlist(pl)
        process_playlist_threads += 1
        # t = threading.Thread(target=get_playlist, args=(pl,))
        # t.daemon = True
        # t.start()

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
                terms = clean_string(track['artist'] + ' ' + track['name'])
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
                    edge_case_search_in = r['title'] + ' ' + r['channel']
                    edge_case_search_in2 = clean_string(edge_case_search_in).lower()
                    unrelated = False
                    r2 = clean_string(search_in).lower()
                    for t in terms_list:
                        t2 = clean_string(t).lower()
                        if len(t) > 1 and r2.find(t2) != -1:
                            matches += 1

                    if required_matches < 4 and matches != required_matches:
                        unrelated = True
                    elif required_matches >= 4:
                        # if a song has a long name, considering words beyond 5 are long,
                        # then percent will be calculated, more than n% will qualify
                        required_words_to_matches = configs['song_selection'][
                                                        'min_percent_threshold'] * required_matches / 100
                        if matches < round(required_words_to_matches):
                            unrelated = True

                        # match_percent = matches * 100 / required_matches
                        # if match_percent < configs['song_selection']['min_percent_threshold']:  # matches less than 60 percent will disqualify

                    # detect edge cases here live, instrumental etc
                    edge_cases = configs['song_selection']['edge_cases']
                    for e in edge_cases:
                        if edge_case_search_in2.find(e.lower()) != -1 and terms.find(e.lower()) == -1:
                            unrelated = True
                            break

                    if not configs['song_selection']['use_filtering']:
                        unrelated = False

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
                    songs_not_found_list.append(pre_text + ', term used: ' + track['search_term'])
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
                track['selected_result'] = selected_result['video_id'] + ' ' + selected_result['title'] + ' I:' + str(
                    result_index) + ' D:' + str(result_diff)

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
            # process_track(pl, folder_path, track, track_index)
            t = threading.Thread(target=process_track, args=(pl, folder_path, track, track_index))
            t.daemon = True
            t.start()

        total_playlist_cd -= 1

    p('Waiting for threads to finish :' + str(running_threads))
    while running_threads != 0:
        print('... Running threads: ' + str(running_threads))
        time.sleep(2)

    p('Checking for removed files')
    diffed_files = diff_files(configs['download_dir'], configs['download_dir'], files=diff_file_paths)

    if len(diffed_files['files_to_remove']):
        p('Removing files')
        process_diff_files(diffed_files, configs['download_dir'], configs['download_dir'])

    sync_drive()

    p('Songs not found: ' + str(len(songs_not_found_list)))
    for s in songs_not_found_list:
        p('not found: ' + s)

    p('Completed')


def sync_drive():
    """
    Sync download drive with sync drives
    :rtype: object
    """
    for drive in configs['sync_download_dir']:
        if os.path.exists(drive):
            p('Syncing files with ' + drive)
            drive_diff_files = diff_files(configs['download_dir'], drive)
            process_diff_files(drive_diff_files, configs['download_dir'], drive)
        else:
            p('The path ' + drive + ' does not exists atm, skipping')


if args.d:
    print('ok')

if args.s:
    process_playlist()

if args.ds:
    sync_drive()
