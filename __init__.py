from adapt.intent import IntentBuilder
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
import subprocess as sp

class BeetsSkill(CommonPlaySkill):
    def __init__(self):
        super().__init__()

    def initialize(self):
        self.add_event('mycroft.audio.service.play', self.handle_play)
        self.add_event('mycroft.audio.service.stop', self.handle_stop)
        self.add_event('mycroft.audio.service.pause', self.handle_pause)
        self.add_event('mycroft.audio.service.resume', self.handle_resume)
        self.add_event('mycroft.audio.service.next', self.handle_next)
        self.add_event('mycroft.audio.service.prev', self.handle_prev)

    def stop(self):
        pass

    def shutdown(self):
        pass

    def handle_play(self):
        pass

    def handle_stop(self):
        pass

    def handle_pause(self):
        pass

    def handle_resume(self):
        pass

    def handle_prev(self):
        pass

    def handle_next(self):
        pass

    def CPS_match_query_phrase(self, phrase):
        pass

    def CPS_start(self, phrase, data):
        pass


def create_skill():
    return BeetsSkill()
