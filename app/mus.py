from pyglet import media
from pyglet import resource
from itertools import cycle
import os

class Mus:
    playlist = None
    player = None
    playlist_data = None

    def __init__(self):
        self.eat = resource.media("resource/system/eat.mp3", streaming=False)
        self.crash = resource.media("resource/system/crash.mp3")
        self.playlist_data = []
        mp3_files = [os.path.join('resource/music', f) for f in os.listdir('resource/music') if f.endswith('.mp3')]
        for filename in mp3_files:
            self.playlist_data.append(resource.media(filename.replace("\\", "/")))

    def play_music(self):
        if self.playlist_data:
            self.playlist = cycle(self.playlist_data)
            self.player = media.Player()
            # self.player.loop = True
            self.player.queue(self.playlist)
            self.player.play()
        
    def close_music(self):
        self.player.pause()
