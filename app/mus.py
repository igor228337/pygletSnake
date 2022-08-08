from pyglet import media
from pyglet import resource
from itertools import cycle


class Mus:
    playlist = None
    player = None

    def __init__(self):
        self.eat = resource.media("resource/eat.mp3", streaming=False)
        self.crash = resource.media("resource/crash.mp3")
        self.bgm1 = resource.media("resource/bgm1.mp3")
        self.bgm2 = resource.media("resource/bgm2.mp3")
        self.bgm3 = resource.media("resource/bgm3.mp3")
        self.bgm4 = resource.media("resource/bgm4.mp3")
        self.bgm5 = resource.media("resource/bgm5.mp3")

    def play_music(self):
        self.playlist = cycle([self.bgm1, self.bgm2, self.bgm3, self.bgm4, self.bgm5])
        self.player = media.Player()
        # self.player.loop = True
        self.player.queue(self.playlist)
        self.player.play()
