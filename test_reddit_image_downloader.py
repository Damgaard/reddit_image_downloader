#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Should be used instead of Exception in test_get_submissions_private_sub and
# test_get_submissions_nonexisting_sub. But weirdly enough it doesn't catch the
# error even though it should be the same.
# from urllib2 import HTTPError

import os

import pytest

from authentication import IMGUR_CLIENT_ID, REDDIT_USERAGENT
from reddit_image_downloader import *


def test_connect_to_imgur():
    im = connect_to_imgur(IMGUR_CLIENT_ID)
    # Test the imgur session is functional
    image = im.get_image('S1jmapR')
    assert image.views > 1


def test_connect_to_imgur_bad_argument():
    # PyImgur uses lazy objects. The imgur session will not be validated until
    # the first request has been made
    im = connect_to_imgur("BAD_CLIENT_ID")
    with pytest.raises(Exception):  # 403. Access Denied.
        image = im.get_image('S1jmapR')
        assert image.views > 1


def test_connect_to_reddit():
    r = connect_to_reddit(REDDIT_USERAGENT)
    sub = r.get_submission(submission_id='16m0uu')
    assert sub.author.name == 'bboe'


def test_get_submissions():
    subreddits = ['pics', 'cats', 'gifs', 'funny']
    reddit_session = connect_to_reddit(REDDIT_USERAGENT)
    posts = get_submissions(reddit_session, subreddits, 'hot')
    assert posts


def test_get_submissions_private_sub():
    subreddits = ['lounge']
    reddit_session = connect_to_reddit(REDDIT_USERAGENT)
    with pytest.raises(Exception):  # 403. Access Denied.
        posts = get_submissions(reddit_session, subreddits)
        assert not posts


def test_get_submissions_nonexisting_sub():
    subreddits = ['notexisting']
    reddit_session = connect_to_reddit(REDDIT_USERAGENT)
    with pytest.raises(Exception):  # 404. Access Denied.
        posts = get_submissions(reddit_session, subreddits)
        assert not posts


def test_is_direct_url():
    assert is_direct_image_link('http://www.imgur.com/n0D2J3C.jpeg')
    assert is_direct_image_link('http://d24w6bsrhbeh9d.cloudfront.net/'
                                'photo/aBK11LA_700b.jpg')  # 9gag
    assert is_direct_image_link('http://www.paradoxplaza.com/sites/all/'
                                'themes/paradoxplaza/logo.png')
    assert is_direct_image_link('http://dota2gifs.com/gifs/EnigmaTI3.gif')
    assert not is_direct_image_link('http://www.reddit.com')
    assert not is_direct_image_link('ftp://http://www.reddit.com')
    assert not is_direct_image_link('')


def test_sanitize_file_name_illegal_chars():
    assert sanitize_filename_windows("HelloWorld?.jpg") == "HelloWorld.jpg"
    assert sanitize_filename_windows("HelloWorld.jpg?") == "HelloWorld.jpg"
    assert sanitize_filename_windows('Hello"World".jpg') == "Hello'World'.jpg"


def test_sanitize_filename_windows_file_name_unicode():
    assert sanitize_filename_windows("HelloWøøørld.jpg?") == "HelloWrld.jpg"


def test_sanitize_filename_windows_file_name_more_readable():
    assert sanitize_filename_windows("Hello World.jpg") == "Hello_World.jpg"


# TODO add proper setup and teardown functions
def test_imgur_download():
    im = connect_to_imgur(IMGUR_CLIENT_ID)
    try:
        name = 'test_download'
        url = 'http://imgur.com/gallery/7RsFUmL'
        result = imgur_download(im, name, url)
        assert len(result) == 1
        assert result[0] == name + ".jpg"
    finally:
        if 'result' in locals():
            for file in result:
                os.remove(file)


def test_imgur_download_album():
    im = connect_to_imgur(IMGUR_CLIENT_ID)
    try:
        name = 'test_download'
        url = 'http://imgur.com/a/9kgGe'
        result = imgur_download(im, name, url)
        assert len(result) == 3
        assert result[0] == name + "_1.jpg"
        assert result[1] == name + "_2.jpg"
        assert result[2] == name + "_3.jpg"
    finally:
        if 'result' in locals():
            for file in result:
                os.remove(file)
