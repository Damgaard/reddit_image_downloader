#!/usr/bin/env python
#
# This file is part of reddit image downloader.
#
# reddit image downlaoder is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# reddit image downloader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# reddit image downloader.  If not, see <http://www.gnu.org/licenses/>.

"""Reddit image downloader

Downloads images from a subreddit.

Usage:
    reddit_image_downloader.py -h | --help
    reddit_image_downloader.py --gui
    reddit_image_downloader.py <subreddit> ... [--hot|--new|--rising] [--nsfw]
                                [--limit=<n>] [--size=<img_size>]
                                [--reddit_name|--reddit_over_id]
                                [--savedir=<n>]
    reddit_image_downloader.py <subreddit> ... (--top|--controversial) [--nsfw]
                                [--limit=<n>] [--time=<period>]
                                [--size=<img_size>]
                                [--reddit_name|--reddit_over_id]
                                [--savedir=<n>]

Options:
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
 --reddit_name      Always set the name to the reddit title
 --reddit_over_id   Set name to reddit title, if image is untitled on imgur.
 --savedir=<n>      The directory to save downloaded files in [default 25]

"""

import shutil
import os
from urlparse import urlparse

from docopt import docopt
import praw
import pyimgur

from view import Terminal

# The maximum amount of submissions that can retrieved from Reddit.com
MAX_SUBMISSIONS = 1000


def main():
    arguments = docopt(__doc__, version='Reddit image downloader 0.1')
    process_arguments(arguments)
    test_valid_arguments(arguments)
    Terminal(arguments, download_images)
    # The view is responsible for running download_images when it wants.
    # Terminal simply runs it upon the end of initialization, but a GUI could
    # choose to first run the function when a user clicks a "run" button.


def download_images(arguments, view):
    """Downloads the images from the subreddits."""
    reddit = praw.Reddit('Reddit image downloader by u/_Daimon_ ver 0.1')
    subreddit = get_subreddit(reddit, arguments)
    listing = get_listing(subreddit, arguments)
    params = {'t': arguments['--time']}
    for sub in listing(limit=arguments['--limit'], url_data=params):
        if not can_be_processed(sub, arguments, view):
            continue
        img_hash = get_img_hash(sub.url)
        try:
            new_image = pyimgur.download_image(img_hash,
                                               size=arguments['--size'])
        except pyimgur.errors.Code404:
            continue
        if arguments['--reddit_name'] or ((new_image.startswith(img_hash)
                                           and arguments['--reddit_over_id'])):
            title = sanitize(sub.title)
            new_name = title + '.' + new_image.split('.')[-1]
            new_name = os.path.join(arguments['--savedir'], new_name)
            if not os.path.exists(new_name):
                shutil.move(new_image, new_name)
        else:
            new_name = os.path.join(arguments['--savedir'], new_image)
            if not os.path.exists(new_name):
                shutil.move(new_image, new_name)


def get_subreddit(reddit, arguments):
    """Return the subreddit object. Raise error if invalid arguments."""
    subreddit_name = "+".join(arguments['<subreddit>'])
    subreddit = reddit.get_subreddit(subreddit_name)
    test_valid_subreddit(subreddit)
    return subreddit


def can_be_processed(submission, arguments, view):
    """Is this a image post we can process?"""
    if submission.is_self or 'imgur.com' not in submission.domain:
        view.not_imgur_domain(submission)
    elif submission.over_18 and not arguments['--nsfw']:
        view.nsfw_submission(submission)
    elif is_album(submission.url):  # Temporary. Should be handled by pyimgur
        view.links_to_album(submission)
    else:
        view.valid_submission(submission)
        return True
    return False


def sanitize(title):
    """Sanitize the title to become part of a valid filename."""
    only_ascii = title.encode('ascii', 'ignore')
    no_bad_char = "".join(ch for ch in only_ascii if ch not in '"?')
    return no_bad_char.strip()


def test_valid_subreddit(subreddit):
    """Test that the subreddit is valid, neccesary due to lazy evaluation."""
    try:
        subreddit.get_hot().next()
    except ValueError as error:
        if error.message == 'No JSON object could be decoded':
            raise ValueError('Invalid subreddit.')
        raise


def get_listing(subreddit, arguments):
    """Return the subreddit listing with the requested form of sorting."""
    if arguments['--new']:
        return subreddit.get_new_by_date
    elif arguments['--rising']:
        return subreddit.get_new_by_rising
    elif arguments['--controversial']:
        return subreddit.get_controversial
    elif arguments['--top']:
        return subreddit.get_top
    else:
        return subreddit.get_hot


def is_album(url):
    """Does the url point to an imgur album rather than an image?"""
    return urlparse(url).fragment


def get_img_hash(url):
    """Return the img_hash from the url."""
    return urlparse(url).path.split('/')[-1].split('.')[0]


def process_arguments(arguments):
    """Process the arguments, so they can be used."""
    arguments['--time'] = arguments['--time'].lower()
    arguments['--size'] = arguments['--size'].lower()
    if arguments['--limit'].lower() == 'none':
        arguments['--limit'] = MAX_SUBMISSIONS
    else:
        arguments['--limit'] = int(arguments['--limit'])
    if arguments['--savedir'] is None:
        arguments['--savedir'] = os.path.abspath('.')


def test_valid_arguments(arguments):
    """Test that argument values are valid, if not raise LookupError."""
    valid_options = {'time': ('hour', 'day', 'week', 'month', 'year', 'all'),
                     'size': ('original', 'small_square', 'large_thumbnail')}
    for option in valid_options:
        if arguments['--%s' % option] not in valid_options[option]:
            raise LookupError("%s must have one of the following values: %s"
                              % (option, " ".join(valid_options[option])))


if __name__ == '__main__':
    main()
