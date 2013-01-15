# Subreddit Image Downloader

Simplifies downloading images from subreddits.

# Usage

reddit\_imag\_downloader.py -h | --help
reddit\_imag\_downloader.py [--hot|--new|--rising] [--nsfw] [--limit=<n>]
reddit\_imag\_downloader.py [--top|--controversial] [--nsfw] [--limit=<n>]
                            [--hour|--day|--week|--month|--year|--year]

**options**

 -h --help          Show help screen.
 --limit            The number of images to download.
 --nsfw             Download NSFW images.
 -s --subreddit     The subreddit to download images from.
 --hot              Get the hottest images (default) from the subreddit.
 --new              Get the newest images from the subreddit.
 --rising           Get the rising images from the subreddit.
 --controversial    Get the controversial images from the subreddit.
 --top              Get the top images from subreddit.
 --hour             Get the images from the last hour.
 --day              Get the images from the last day.
 --week             Get the images from the last week.
 --month            Get the images from the last month.
 --year             Get the images from the last year.
 --all              Get the images from all time.

# Dependencies

docopt, praw and pyimgur. Install them with pip

```python
pip install docopt
pip install praw
pip install pyimgur
```
