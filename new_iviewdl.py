#!/usr/bin/env python
try:
  from urllib2 import urlopen
except ImportError:
  from urllib.request import urlopen
import json
import argparse
from youtube_dl import YoutubeDL

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("seriesurl", help="The url to the series you'd like to download, e.g https://iview.abc.net.au/show/shaun-micallefs-mad-as-hell/series/9")
    args = parser.parse_args()
    page = urlopen(args.seriesurl).read().split(b"window.__INITIAL_STATE__ = ",1)[1].split(b";")[0]
    data = json.loads(eval(page))
    with YoutubeDL({"outtmpl": "%(series)s %(season_number)sx%(episode_number)s %(title)s.%(ext)s", "external_downloader": "ffmpeg", "external_downloader_args": ["-v", "quiet", "-stats"]}) as ydl:
        ydl.download([ep["shareUrl"] for ep in data["page"]["pageData"]["_embedded"]["selectedSeries"]["_embedded"]["videoEpisodes"]])

if __name__ == "__main__":
    main()
