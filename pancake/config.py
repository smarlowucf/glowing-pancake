import os


class Config(object):
    def __init__(self, testing=False):
        self.TESTING = testing

    @property
    def PANCAKE_DB(self):
        return os.path.expanduser('~/pancakes.json')
