#!/usr/bin/env python
try:
  from urllib2 import urlopen
except ImportError:
  from urllib.request import urlopen
import json
import argparse
from youtube_dl import YoutubeDL

def download_url_list(urllist):
    with YoutubeDL({"outtmpl": "%(series)s %(season_number)sx%(episode_number)s %(title)s.%(ext)s", "external_downloader": "ffmpeg", "external_downloader_args": ["-v", "quiet", "-stats"]}) as ydl:
        ydl.download(urllist)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("seriesurl", help="The url to the series you'd like to download, e.g https://iview.abc.net.au/show/shaun-micallefs-mad-as-hell/series/9")
    args = parser.parse_args()
    if "/video/" in args.seriesurl:
        download_url_list([args.seriesurl])
    else:
        page = urlopen(args.seriesurl).read().split(b"window.__INITIAL_STATE__ = ",1)[1].split(b";")[0]
        data = json.loads(eval(page))
        download_url_list([ep["shareUrl"] for ep in data["route"]["pageData"]["_embedded"]["selectedSeries"]["_embedded"]["videoEpisodes"]])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Aborted.")
