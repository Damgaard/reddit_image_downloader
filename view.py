"""Holds the various views for reddit image downloader."""


class Terminal:
    def __init__(self, arguments, download_images_func):
        self.arguments = arguments
        download_images_func(arguments, self)

    def not_imgur_domain(self, submission):
        pass

    def nsfw_submission(self, submission):
        pass

    def links_to_album(self, submission):
        pass

    def valid_submission(self, submission):
        pass
