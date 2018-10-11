#!/usr/bin/env python
from youtube_dl import YoutubeDL
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator

class Yt2Rss:
    def build(self, opts):
        """

        :param opts:
        :param opts['playlist_url']: string
        :param opts['min_duration']: integer, seconds
        :return: string xml rss
        """
        if not opts['playlist_url']:
            raise Exception("no playlist url provided")

        playlist_json = self.get_playlist_json(opts['playlist_url'])
        feed_generator = self.init_feed(playlist_json)

        for entry in playlist_json['entries']:
            if not entry:
                continue
            if opts['min_duration'] and opts['min_duration'] > entry['duration']:
                continue
            self.set_image(feed_generator, entry)
            self.add_entry(feed_generator, entry)

        return feed_generator.rss_str(pretty=True)

    def set_image(self, feed, entry):
        '''
        set rss feed icon if it's not been set yet
        '''
        if entry['thumbnail'] is not None and feed.logo() is None:
            feed.logo(entry['thumbnail'])

    def get_playlist_json(self, playlist_url):
        ytdl_opts = {
            'playlistend': 10,
            'dump_single_json': True,
            'simulate': True,
            'quiet': True,
            'ignoreerrors': True,
            'format': 'best[protocol^=http]'
        }
        yt = YoutubeDL(ytdl_opts)

        res = yt.extract_info(playlist_url)
        return res

    def init_feed(self, playlist):
        fg = FeedGenerator()
        fg.load_extension('podcast')

        fg.id(playlist['webpage_url'])

        if playlist['title']:
            fg.title(playlist['title'])
            fg.description(playlist['title'])

        link = {
            'href': playlist['webpage_url'],
            'rel': 'alternate'
        }
        fg.link(link)
        return fg

    def add_entry(self, fg, entry):
        """
        :type fg: FeedGenerator

        res.title
        res.webpage_url
        res.entries[]
            id
            upload_date
            title
            duration
            thumbnail
            webpage_url
            description
            url
        """
        fe = fg.add_entry()
        fe.enclosure(entry['url'], 0, 'video/mp4')
        upload_date = self._upload_date_to_datetime(entry['upload_date'])
        fe.published(upload_date)
        fe.title(entry['title'])
        fe.id(entry['id'])
        fe.podcast.itunes_duration(entry['duration'])
        fe.description(entry['description'])

        link = {
            'href': entry['webpage_url'],
            'rel': 'alternate'
        }
        fe.link(link)
        '''fe.podcast.itunes_image(entry['thumbnail'])'''

    def _upload_date_to_datetime(self, upload_date):
        '''
        Return a datetime object at noon (UTC) for the given date.
        :param upload_date: string YYYYMMDD
        :return:
        '''
        return datetime(int(upload_date[:4]), int(upload_date[4:6]), int(upload_date[6:]), 12, tzinfo=timezone.utc)
