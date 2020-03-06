#!/usr/bin/env python
from __future__ import unicode_literals

# Execute with
# $ python3 -m yt2pod

import sys
from optparse import OptionParser
import ytdl2rss
import os.path

if __package__ is None and not hasattr(sys, 'frozen'):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--base-dir", dest="base_dir",
                      help="file system path where the playlists will be downloaded to")
    parser.add_option("-u", "--url", dest="playlist_url",
                      help="url of the podcast")
    parser.add_option("-n", "--name", dest="playlist_name",
                      help="short name of the podcast for URL ")
    parser.add_option("-d", "--min-duration", dest="min_duration",
                      help="minimum duration for each episode")

    (options, args) = parser.parse_args()

    opts = {
        'playlist_url': options.playlist_url,
        'playlist_name': options.playlist_name,
        'base_dir': options.base_dir,
        'base_url': 'http://ubi.fritz.box:8080/podcast/'
    }

    if options.min_duration:
        opts['min_duration'] = int(options.min_duration)

    ytdl = ytdl2rss.Yt2Rss()
    xmlstring = ytdl.build(opts)

if __name__ == '__main__':
    main()
