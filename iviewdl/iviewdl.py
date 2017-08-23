#!/usr/bin/env python
from __future__ import print_function
from distutils.spawn import find_executable
import re
import sys
from tempfile import NamedTemporaryFile

from bs4 import BeautifulSoup as Soup
import requests

if sys.version_info[0] == 3:
    unicode = str

if not find_executable("ffmpeg"):
    print("You need to install ffmpeg. apt install ffmpeg / yum install ffmpeg")
    sys.exit(1)
TOKEN = Soup(requests.get("http://iview.abc.net.au/auth").text, "lxml").find("tokenhd").text

def search(term):
    return requests.get("http://iview.abc.net.au/api/search/", params={"fields": "href,seriesTitle,title", "keyword": term}).json()

def vtt_to_srt(url):
    vtt = requests.get(url).text.strip()
    out = []
    for n,block in enumerate(vtt.split("\n\n")[1:]):
        out.append("{}\n{}".format(n,block.strip()))
    with NamedTemporaryFile(delete=False, suffix=".srt") as temp:
        temp.write(unicode("\n\n".join(out)).encode("utf-8"))
        temp.seek(0)
        return temp.name

def fix_stream_url(url):
    return url.replace("iviewhls-i.akamaihd", "iviewum-vh.akamaihd") + "?hdnea" + TOKEN

def get_stream_urls(data):
    if data["playlist"]:
        out = {}
        out["filename"] = "".join(c if c not in "\/:*?<>|" else "_" for c in "{} {}.mp4".format(data["seriesTitle"], data["title"]))
        for p in data["playlist"]:
            if p["type"] == "program":
                out["program"] = fix_stream_url(p["hls-high"])
                if "captions" in p:
                    out["subs"] = vtt_to_srt(p["captions"]["src-vtt"])
            elif p["type"] == "rating":
                out["rating"] = fix_stream_url(p["hls-high"])
            elif p["type"] == "preroll":
                out["rating"] = fix_stream_url(p["hls-high"])
        return out
    else:
        raise Exception("No playlist data")

def get_download_cmd(urls, filename=None):
    out = ["ffmpeg"]
    out += ["-i", urls["program"]]
    if "subs" in urls:
        out += ["-i", urls["subs"]]
    out += ["-c:v", "copy", "-c:a", "copy", "-bsf:a", "aac_adtstoasc"]
    out += ["-map", "0:0", "-map", "0:1"]
    if "subs" in urls:
        out += ["-map", "1", "-c:s:0", "mov_text", "-metadata:s:s:0", "language=eng"]
    out += [urls["filename"]]
    return out

def prompt(question, response_type=int):
    index = None
    while index is None:
        try:
            index = response_type(input(question))
        except ValueError:
            print("Try again. Has to be a number.")
        except IndexError:
            print("Check your input. Ctrl-C to back out")
        except KeyboardInterrupt:
            print("\nAborted")
            exit(127)
    return index

def main():
    from argparse import ArgumentParser
    import subprocess
    parser = ArgumentParser()
    parser.add_argument("search")
    parser.add_argument("-s", "--selection", help="Number of video to get", type=int)
    parser.add_argument("-f", "--filename")
    args = parser.parse_args()
    results = search(args.search)
    if len(results) > 1:
        if args.selection is None:
            print("\n".join("{0}: {seriesTitle} {title}".format(n, **data) for n,data in enumerate(results)))
            if sys.stdout.isatty():
                result = results[prompt("enter your choice: ")]
            else:
                return 2
        else:
            result = results[args.selection]
    else:
        result = results[0]
    print("Downloading {seriesTitle} {title}".format(**result), file=sys.stdout)
    data = get_stream_urls(requests.get("http://iview.abc.net.au/api/" + result["href"]).json())
    process = subprocess.Popen(get_download_cmd(data, filename=args.filename), stdout=subprocess.PIPE)
    process.wait()
    return process.returncode

if __name__ == "__main__":
    sys.exit(main())
