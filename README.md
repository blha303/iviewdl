This project is deprecated, just use youtube-dl
===================

If you'd like to adopt this project please open an issue. All current bugs won't be fixed by blha303. Sorry.

Get the url from iview using the Share button under an episode, copy the link
```bash
$ pip install youtube-dl 
$ youtube-dl https://iview.abc.net.au/show/shaun-micallefs-mad-as-hell/series/9/video/LE1814V001S00
```

iviewdl
=======

**Working again as of 15 August 2018**

A Python program to download videos from ABC iView. **Requires ffmpeg installed**

Usage
-----

* `pip install git+https://github.com/blha303/iviewdl`
* `iviewdl micallef`
  * If there is more than one result, it will return a list, re-run the command with `--selection [n]` to pick
* Pass `--filename=[fn]` to set the filename

Contributing
------------

Open `iviewdl/iviewdl.py`, have a look, it's pretty straightforward. I don't want to be the only person that knows how the site works, there needs to be clients in more languages than Python. If there's a bug to fix or more features to add, please submit an issue or a pull request.

Forks
-----

[bobri/iviewdl](https://github.com/bobri/iviewdl) - Adds feature to batch download from a list of urls in a file (#7)
