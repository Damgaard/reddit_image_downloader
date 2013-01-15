"""Reddit img downloader

Downloads images from a subreddit.

Usage:
    reddit_img_downloader.py -h | --help
    reddit_img_downloader.py <subreddit> ... [--hot|--new|--rising] [--nsfw]
                                [--limit=<n>]
    reddit_img_downloader.py <subreddit> ... [--top|--controversial]
                                [--hour|--day|--week|--month|--year|--all]
                                [--nsfw] [--limit=<n>]

Options:
 -h --help          Show help screen.
 --limit=<n>        The number of images to download [default: 25].
 --nsfw             Download NSFW images.
 --subreddit        The subreddit(s) to download images from.
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

"""

from docopt import docopt
import praw
import pyimgur

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Reddit img downloader 0.1')
    print arguments
