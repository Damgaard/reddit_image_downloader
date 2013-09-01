Reddit Image Downloader
=======================

Simplifies downloading images from subreddits.

Usage
-----

.. code-block:: text

  Reddit image downloader

  Downloads images from a subreddit.

  Usage:
      reddit_image_downloader.py -h | --help
      reddit_image_downloader.py <subreddit> ... [--hot|--new|--rising]
                                  [--limit=<n>]
      reddit_image_downloader.py <subreddit> ... (--top|--controversial)
                                  [--limit=<n>] [--time=<period>]

  Options:
  -h --help          Show help screen.
  --subreddit        The subreddit(s) to download images from.
  --hot              Get the hottest images (default) from the subreddit.
  --new              Get the newest images from the subreddit.
  --rising           Get the rising images from the subreddit.
  --controversial    Get the controversial images from the subreddit.
  --top              Get the top images from subreddit.
  --limit=<n>        The number of images to download [default: 25].
  --time=<period>    The time period to look at [default: day].

Dependencies
------------

Reddit\_Image\_Downloader's dependencies can be found in requirements.txt. To
install all dependencies.

.. code-block:: bash

  $ pip install -r requirements.txt

License
-------

All of the code contained here is licensed by the GNU GPLv3.
