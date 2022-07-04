from adapt.intent import IntentBuilder
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.skills.audioservice import AudioService
import subprocess as sp
from mpd import MPDClient
from contextlib import contextmanager


class BeetsSkill(CommonPlaySkill):
    def __init__(self):
        super().__init__()
        self.genres = set()
        self.client = MPDClient()

    def initialize(self):
        self.add_event('mycroft.audio.service.play', self.handle_play)
        self.add_event('mycroft.audio.service.stop', self.handle_stop)
        self.add_event('mycroft.audio.service.pause', self.handle_pause)
        self.add_event('mycroft.audio.service.resume', self.handle_resume)
        self.add_event('mycroft.audio.service.next', self.handle_next)
        self.add_event('mycroft.audio.service.prev', self.handle_prev)
        self.get_genres()

    @contextmanager
    def connection(self):
        try:
            self.client.connect('localhost', 6600)
            yield
        finally:
            self.client.close()
            self.client.disconnect()

    def stop(self):
        pass

    def handle_play(self):
        pass

    def handle_stop(self):
        with self.connection():
            self.client.stop()

    def handle_pause(self):
        with self.connection():
            self.client.pause(1)

    def handle_resume(self):
        with self.connection():
            self.client.pause(0)

    def handle_prev(self):
        with self.connection():
            self.client.previous()

    def handle_next(self):
        with self.connection():
            self.client.next()

    def CPS_match_query_phrase(self, phrase):
        phrase = phrase.lower()
        if ' by ' in phrase:
            (first, second) = phrase.split(' by ')
            # Title by Artist
            (title, artist) = (first, second)
            output = self.find_music(title=title, artist=artist)
            if output:
                output = [output.split('\n')[0]]
                return ('title:' + title + 'artist:' + artist,
                        CPSMatchLevel.MULTI_KEY,
                        output)

            # Album by Artist
            (album, artist) = (first, second)
            output = self.find_music(album=album, artist=artist)
            if output:
                return ('album:' + album + 'artist:' + artist,
                        CPSMatchLevel.MULTI_KEY,
                        output.split('\n'))

        # Genre
        if 'genre' in phrase:
            for genre in self.genres:
                if genre and genre.lower() in phrase:
                    output = self.find_music(genre=genre)
                    if output:
                        return ('genre:' + genre,
                                CPSMatchLevel.CATEGORY,
                                output.split('\n'))

        # Album
        output = self.find_music(album=phrase)
        if output:
            return ('album:' + phrase,
                    CPSMatchLevel.TITLE,
                    output.split('\n'))

        # Title
        output = self.find_music(title=phrase)
        if output:
            output = [output.split('\n')[0]]
            return ('title:' + phrase,
                    CPSMatchLevel.TITLE,
                    output)

        # Artist
        output = self.find_music(artist=phrase)
        if output:
            return ('artist:' + phrase,
                    CPSMatchLevel.ARTIST,
                    output.split('\n'))

        # Anything
        output = self.find_music(artist=phrase)
        if output:
            return (phrase,
                    CPSMatchLevel.GENERIC,
                    output.split('\n'))

        return None

    def find_music(self, title=None, album=None, artist=None, genre=None):
        if not title and not artist and not album and not genre:
            return None
        query = 'beet list -p'
        if title:
            query += ' title:' + title
        if album:
            query += ' album:' + album
        if artist:
            query += ' artist:' + artist
        if genre:
            query += ' genre:' + genre
        query = query.split()
        process = sp.run(query, capture_output=True, timeout=3,
                         encoding='utf-8')
        return process.stdout

    def CPS_start(self, phrase, data):
        with self.connection():
            songid = None
            for file_path in data:
                file_path = file_path.strip()
                if not file_path:
                    continue
                file_path = 'file://' + file_path
                if not songid:
                    songid = self.client.addid(file_path)
                else:
                    self.client.addid(file_path)
            self.client.playid(songid)

    def get_genres(self):
        query = 'beet list -f \'$genre\''
        process = sp.run(query.split(' '), capture_output=True, timeout=3,
                         encoding='utf-8')
        for genre in set(process.stdout.split('\n')):
            self.genres.add(genre.replace('\'', ''))


def create_skill():
    return BeetsSkill()
