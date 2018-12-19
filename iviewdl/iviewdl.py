#!/usr/bin/env python
from __future__ import print_function
from distutils.spawn import find_executable
import time
import sys
from tempfile import NamedTemporaryFile
import hmac
import hashlib
import requests
from argparse import ArgumentParser
import subprocess

if sys.version_info[0] == 3:
    unicode = str

if not find_executable("ffmpeg"):
    print("You need to install ffmpeg. apt install ffmpeg / yum install ffmpeg")
    sys.exit(1)


def search(term):
    return requests.get("http://iview.abc.net.au/api/search/",
                        params={"fields": "href,seriesTitle,title", "keyword": term}).json()


def vtt_to_srt(url):
    vtt = requests.get(url).text.strip()
    out = []
    for n, block in enumerate(vtt.split("\n\n")[1:]):
        out.append(u"{}\n{}".format(n, block.strip()))
    with NamedTemporaryFile(delete=False, suffix=".srt") as temp:
        temp.write(unicode("\n\n".join(out)).encode("utf-8"))
        temp.seek(0)
        return temp.name


def generate_secret(movieid):
    urlparam = "/auth/hls/sign?ts={}&hn={}&d=(null)".format("%.6f" % time.time(), movieid)
    message = bytes(urlparam)
    secret = bytes("MainContainerViewController")
    sig = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()
    abc_2nd_url = "http://iview.abc.net.au" + urlparam + "&sig=" + sig
    final_request = requests.get(abc_2nd_url)
    return "?hdnea=" + final_request.content


def get_stream_urls(data):
    if data["playlist"]:
        if "title" not in data:  # title must exist for the file name
            data["title"] = ""
        else:
            data["title"] = " " + data["title"]

        out = {"filename": "".join(
            c if c not in "\/:*?<>|" else "_" for c in "{}{}.mp4".format(data["seriesTitle"], data["title"]))}
        for p in data["playlist"]:
            if p["type"] == "program":
                out["program"] = p["hls-plus"] + generate_secret(data["episodeHouseNumber"])
                if "captions" in p:
                    out["subs"] = vtt_to_srt(p["captions"]["src-vtt"])
            elif p["type"] == "rating":
                out["rating"] = p["hls-plus"] + generate_secret(data["episodeHouseNumber"])
            elif p["type"] == "preroll":
                out["rating"] = p["hls-plus"] + generate_secret(data["episodeHouseNumber"])
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
    out += [urls["filename"]] if filename is None else [filename]
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
    parser = ArgumentParser()
    parser.add_argument("search")
    parser.add_argument("-s", "--selection", help="Number of video to get", type=int)
    parser.add_argument("-f", "--filename")
    args = parser.parse_args()
    results = search(args.search)
    if len(results) > 1:
        if args.selection is None:
            for n, data in enumerate(results):
                try:
                    print("{0}: {seriesTitle} {title}".format(n, **data))
                except KeyError:
                    print("{0}: {seriesTitle}".format(n, **data))

            if sys.stdout.isatty():
                result = results[prompt("enter your choice: ")]
            else:
                return 2
        else:
            result = results[args.selection]
    else:
        try:
            result = results[0]
        except IndexError:
            print("No matches found")
            quit()
    try:
        print("Downloading {seriesTitle} {title}".format(**result), file=sys.stdout)
    except KeyError:
        print("Downloading {seriesTitle}".format(**result), file=sys.stdout)
    data = get_stream_urls(requests.get("http://iview.abc.net.au/api/" + result["href"]).json())
    process = subprocess.Popen(get_download_cmd(data, filename=args.filename), stdout=subprocess.PIPE)
    process.wait()
    return process.returncode


if __name__ == "__main__":
    sys.exit(main())
