#!python


"""
simple_web_poller: retrieve, display or store a web site's contents on stdout or Redis at {keyname}.body.

version 0.1.0: initial version.
"""

__desc__ = """
simple_web_poller: retrieve and display or store a web site's contents on stdout or Redis at {keyname}.body.

USAGE: python simple_web_poller [-r|--redis -k|--key keyname] [-f|--frequency seconds] [-h|--help] url

-r, --redis: (optional) log values to redis, otherwise stdout
-k, --key keyname: non-optional if using --redis. Key to store the document's contents in.
-f, --frequency: (optional) number of seconds between samples, if omitted, run once and exit.
"""

__author__ = "Rob Campbell"
__version__ = "0.1.0"
__license__ = "The Unlicense"

import argparse
import socket
import redis
import urllib.request
import sched, time
import math
import subprocess

def get_document_contents(address):
    with urllib.request.urlopen(address) as response:
        body = response.read()
    return body

def write_to_redis():
    key = args.key
    contents = get_document_contents(args.url)
    
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set(key + '.body', contents)
    r.set(key + '.time', time.asctime(time.localtime()))

def write_to_console():
    "probably no key = args.key"
    contents = get_document_contents(args.url)
    print("Body: {}".format(contents))
    print("Time: {}".format(time.asctime(time.localtime())))

def main(args):
    """ Main entry point of the app """

    freq = args.frequency
    scheduler = sched.scheduler()

    if args.redis:
        action = write_to_redis
    else:
        action = write_to_console

    print("simple_web_poller starting up, retrieving {}, storing on {}".format(args.url, args.key))
    print(args)

    # First one is free!
    action()

    while freq > 0:
        # print("simple_web_poller, scheduler loop tick")
        scheduler.enter(freq, 1, action)
        
        scheduler.run()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(usage=__desc__)

    # Optional argument flag which defaults to False
    parser.add_argument("-r", "--redis", help="store values in redis", action="store_true")

    parser.add_argument("-k", "--key", help="key name to store document's contents in", type=str, default="")

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-f", "--frequency", help="set frequency in seconds, if omitted, run once and exit", type=int, default=0)

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    
    parser.add_argument("url", help="the address of the web content to retrieve", type=str)

    args = parser.parse_args()
    main(args)
