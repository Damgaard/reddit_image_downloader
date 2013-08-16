#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
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

"""

from __future__ import unicode_literals

import sys
import traceback

from docopt import docopt
import praw
import pyimgur
import requests

from authentication import IMGUR_CLIENT_ID, REDDIT_USERAGENT


def parse_commandline_args():
    """Verify and parse the commandline arguments."""
    options = docopt(__doc__)
    subreddits = options['<subreddit>']
    listing_options = ('hot', 'top', 'controversial', 'rising', 'new')
    listing = next((op for op in listing_options if options["--" + op]), 'hot')
    time_options = ('hour', 'day', 'week', 'month', 'year', 'all')
    time = options['--time'] if options['--time'] in time_options else 'day'
    limit = int(options['--limit'])
    return subreddits, listing, time, limit


def main():
    subreddits, listing, time, limit = parse_commandline_args()
    im = connect_to_imgur(IMGUR_CLIENT_ID)
    r = connect_to_reddit(REDDIT_USERAGENT)
    submissions = get_submissions(r, subreddits, listing=listing, time=time,
                                  limit=limit)
    new_images = []
    for submission in submissions:
        try:
            name = sanitize_filename_windows(submission.title)
            if is_direct_image_link(submission.url):
                ext = submission.url.rpartition('.')[-1].lower()
                name += "." + ext
                with open(name, 'wb') as outfile:
                    binary_image = requests.get(submission.url).content
                    outfile.write(binary_image)
                new_images.append(name)
            elif im.is_imgur_url(submission.url):
                new_images += imgur_download(im, name, submission.url)
        except Exception:
            print "-------------Error------------------"
            traceback.print_exc()
            sys.stderr.write("Link: " + submission.short_link + "\n")
            sys.stderr.write("Url: " + submission.url + "\n")
            sys.stderr.write("Subreddit: " + str(submission.subreddit) + "\n")
            print "------------------------------------"
    print "\n".join(new_images)


def connect_to_imgur(client_id):
    """Return a connected Imgur session."""
    return pyimgur.Imgur(client_id)


def connect_to_reddit(useragent):
    """Return a connected Reddit session."""
    return praw.Reddit(useragent)


def is_direct_image_link(url):
    """Return whether the url is a direct link to an image."""
    image_extensions = ('jpg', 'jpeg', 'png', 'gif', 'apng', 'tiff', 'bmp')
    return url.rpartition('.')[-1].lower() in image_extensions


def imgur_download(imgur_session, name, url):
    """Download the Imgur image located at url and save it as name.

    If it's an album and it has more than one image, then each image will be
    saved as the name with a suffix. Which consists of a underscore followed by
    the place of the image in the album. I.e. the suffix will be _1 for the
    first image, _2 for the second and so forth.
    """
    obj = imgur_session.get_at_url(url)
    images = obj.images if isinstance(obj, pyimgur.Album) else [obj]
    results = []
    for index, image in enumerate(images, 1):
        new_name = name if len(images) == 1 else name + "_{}".format(index)
        results.append(image.download(name=new_name))
    return results


def sanitize_filename_windows(name):
    """Turn the filename into a legal windows filename.

    See http://support.grouplogic.com/?p=1607
    """
    name = name.decode('utf-8')
    name = name.encode('ascii', 'ignore')
    name = name.replace('"', "'")
    name = name.replace(" ", "_")  # Personal preference
    name = "".join(ch for ch in name if ch not in "^/?<>\:*|”")
    return name[:255]


def get_submissions(reddit_session, subreddits, listing, time=None,
                    limit=0):
    """Return the limit submissions made to subreddit's listing."""
    multi_reddit_name = "+".join(subreddits)
    multi_reddit = reddit_session.get_subreddit(multi_reddit_name)
    # TODO. See if there is a way to optimize this. Looks repetitive
    listings_methods = {'controversial': multi_reddit.get_controversial,
                        'hot': multi_reddit.get_hot,
                        'new': multi_reddit.get_new,
                        'rising': multi_reddit.get_rising,
                        'top': multi_reddit.get_top}
    # Assume listing is always set to a valid option
    method = listings_methods.get(listing)
    return list(method(limit=limit, params={'t': time}))


if __name__ == '__main__':
    main()
