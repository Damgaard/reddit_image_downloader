"""Holds the various views for reddit image downloader."""

class Terminal:
    def __init__(self, arguments, download_images_func):
        self.arguments = arguments
        download_images_func(arguments, self)
