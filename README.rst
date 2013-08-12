Reddit Image Downloader
=======================

Simplifies downloading images from subreddits.

Usage
-----

.. code-block:: text

  reddit\_image\_downloader.py -h | --help
  reddit\_image\_downloader.py --gui
  reddit\_image\_downloader.py <subreddit> ... [--hot|--new|--rising] [--nsfw]
                              [--limit=<n>] [--size=<img_size>]
                              [--reddit_name|--reddit_over_id]
                              [--savedir=<n>]
  reddit\_image\_downloader.py <subreddit> ... (--top|--controversial) [--nsfw]
                              [--limit=<n>] [--time=<period>]
                              [--size=<img_size>]
                              [--reddit_name|--reddit_over_id]
                              [--savedir=<n>]

  **options**
   -h --help          Show help screen.
   --gui              Launch GUI instead of CLI.
   --subreddit        The subreddit(s) to download images from.
   --hot              Get the hottest images (default) from the subreddit.
   --new              Get the newest images from the subreddit.
   --rising           Get the rising images from the subreddit.
   --controversial    Get the controversial images from the subreddit.
   --top              Get the top images from subreddit.
   --nsfw             Allow download of NSFW images.
   --limit=<n>        The number of images to download [default: 25].
   --time=<period>    The time period to look at [default: day].
   --size=<img_size>  The size of the images to download [default: original].
   --reddit\_name      Always set the name to the reddit title
   --reddit\_over\_id   Set name to reddit title, if image is untitled on imgur.
   --savedir=<n>      The directory downloaded files will be saved to [default 25]

Dependencies
------------

Reddit\_Image\_Downloader's dependencies can be found in requirements.txt. To
install all dependencies.

.. code-block:: bash

  $ pip install -r requirements.txt

License
-------

All of the code contained here is licensed by the GNU GPLv3.
