iviewdl
=======

The fancy package has been replaced by a single script! [new_iviewdl.py](new_iviewdl.py)

Depends on ffmpeg and youtube-dl

Old readme
----------

A Python program to download videos from ABC iView. **Requires ffmpeg installed**

Usage
-----

* `pip install git+https://github.com/blha303/iviewdl`
* `iviewdl micallef`
  * If there is more than one result, it will return a list, re-run the command with `--selection [n]` to pick
* Pass `--filename=[fn]` to set the filename

Contributing
------------

~~Open `iviewdl/iviewdl.py`, have a look, it's pretty straightforward. I don't want to be the only person that knows how the site works, there needs to be clients in more languages than Python. If there's a bug to fix or more features to add, please submit an issue or a pull request.~~

Forks
-----

[bobri/iviewdl](https://github.com/bobri/iviewdl) - Adds feature to batch download from a list of urls in a file (#7)
