import os
from configparser import RawConfigParser


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

env = RawConfigParser()
env.read(BASE_DIR + '/env.ini')

FEED_HOST = env['feed']['host']
FEED_PORT = env['feed']['port']
