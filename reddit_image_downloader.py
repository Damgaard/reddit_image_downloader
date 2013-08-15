#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import traceback

import praw
import pyimgur
import requests

from authentication import IMGUR_CLIENT_ID, REDDIT_USERAGENT


def main():
    im = connect_to_imgur(IMGUR_CLIENT_ID)
    r = connect_to_reddit(REDDIT_USERAGENT)
    subreddit = ('cats', 'funny', 'pics')
    submissions = get_submissions(r, subreddit)
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
    """Return whether the url a direct link to an image."""
    image_extensions = ('jpg', 'jpeg', 'png', 'gif', 'apng', 'tiff', 'bmp')
    return url.rpartition('.')[-1].lower() in image_extensions


def imgur_download(imgur_session, name, url):
    """Download the Imgur image located at url and save it as name.

    If it's an album subsequent images will have an underscore and a sequential
    number as a suffix."""
    obj = imgur_session.get_at_url(url)
    images = obj.images if isinstance(obj, pyimgur.Album) else [obj]
    results = []
    for index, image in enumerate(images, 1):
        new_name = name if len(images) == 1 else name + "_{}".format(index)
        results.append(image.download(name=new_name))
    return results


def sanitize_filename_windows(name):
    """Turn the filename into a legal filename.

    See http://support.grouplogic.com/?p=1607
    """
    name = name.decode('utf-8')
    name = name.encode('ascii', 'ignore')
    name = name.replace('"', "'")
    name = name.replace(" ", "_")  # Personal preference
    name = "".join(ch for ch in name if ch not in "^/?<>\:*|”")
    return name[:255]


def get_submissions(reddit_session, subreddits, listing='new', limit=3):
    """Return the limit submissions made to subreddits' listing."""
    multi_reddit_name = "+".join(subreddits)
    multi_reddit = reddit_session.get_subreddit(multi_reddit_name)
    # TODO. See if there is a way to optimize this. Looks repetitive
    listings_methods = {'controversial': multi_reddit.get_controversial,
                        'hot': multi_reddit.get_hot,
                        'new': multi_reddit.get_new,
                        'rising': multi_reddit.get_rising,
                        'top': multi_reddit.get_top}
    method = listings_methods.get(listing, multi_reddit.get_new)
    return list(method(limit=limit))


if __name__ == '__main__':
    main()
