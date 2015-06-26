__author__ = 'alex'
import json


class _Settings(object):
    def __init__(self):
        with open("settings.json") as config_file:
            self.config = json.load(config_file)


config = _Settings().config