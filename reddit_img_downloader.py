"""Reddit img downloader

Downloads images from a subreddit.

Usage:
    reddit_img_downloader.py -h | --help
    reddit_img_downloader.py -gui
    reddit_img_downloader.py <subreddit> ... [--hot|--new|--rising] [--nsfw]
                                [--limit=<n>] [--size=<img_size>]
                                [--reddit_name|--reddit_over_id]
                                [--savedir=<n>]
    reddit_img_downloader.py <subreddit> ... (--top|--controversial) [--nsfw]
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
 --savedir=<n>      The directory downloaded files will be saved to [default 25]

"""

import shutil
import os
from urlparse import urlparse

from docopt import docopt
import praw
import pyimgur

def main(arguments):
    r = praw.Reddit('Reddit img downloader by u/_Daimon_ ver 0.1')
    subreddit_name = make_multireddit(arguments['<subreddit>'])
    subreddit = r.get_subreddit(subreddit_name)
    test_valid_subreddit(subreddit)
    listing = get_listing(subreddit, arguments['--hot'], arguments['--new'],
                          arguments['--rising'], arguments['--controversial'],
                          arguments['--top'])
    params = {'t': arguments['--time']}
    if arguments['--savedir'] is None:
        save_path = os.path.abspath('.')
    else:
        save_path = os.path.abspath(arguments['--savedir'])
    for sub in listing(limit=int(arguments['--limit']), url_data=params):
        if sub.is_self or 'imgur.com' not in sub.domain:
            continue
        if sub.over_18 and not arguments['--nsfw']:
            continue
        if is_album(sub.url):  # Temporary. This should be handled by pyimgur
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
            new_name = os.path.join(save_path, new_name)
            if not os.path.exists(new_name):
                os.rename(new_image, new_name)
        else:
            new_name = os.path.join(save_path, new_image)
            shutil.move(new_image, new_name)

def sanitize(title):
    return title.encode('ascii', 'ignore').replace('"', '')

def make_multireddit(subreddit_list):
    return "+".join(subreddit_list)

def test_valid_subreddit(subreddit):
    """Test that the subreddit is valid, neccesary due to lazy evaluation."""
    try:
        subreddit.get_hot().next()
    except ValueError as e:
        if e.message == 'No JSON object could be decoded':
            raise ValueError('Invalid subreddit.')
        raise

def get_listing(subreddit, is_hot, is_new, is_rising, is_controversial,
                is_top):
    if is_new:
        return subreddit.get_new_by_date
    elif is_rising:
        return subreddit.get_new_by_rising
    elif is_controversial:
        return subreddit.get_controversial
    elif is_top:
        return subreddit.get_top
    else:
        return subreddit.get_hot

def is_album(url):
    return urlparse(url).fragment

def get_img_hash(url):
    return urlparse(url).path.split('/')[-1].split('.')[0]

def test_valid_arguments(arguments):
    """Test that argument values are valid, if not raise LookupError."""
    valid_options = {'time': ('hour', 'day', 'week', 'month', 'year', 'all'),
                     'size': ('original', 'small_square', 'large_thumbnail')}
    for option in valid_options:
        if arguments['--%s' % option] not in valid_options[option]:
            raise LookupError("%s must have one of the following values: %s"
                              % (option, " ".join(valid_options[option])))

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Reddit img downloader 0.1')
    test_valid_arguments(arguments)
    print arguments
    main(arguments)
