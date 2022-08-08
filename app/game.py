from pyglet.window import Window
from random import randint
from pyglet import text, image
from mus import Mus
from pyglet import app


class Game:
    change_to = None
    direction = None
    snk_dy = None
    tail = None
    is_game = None
    snk_dx = None
    snk_y = None
    snk_x = None
    cell_size = 20
    fd_x = None
    fd_y = None
    img = None

    def __init__(self):
        self.window = Window(fullscreen=True)
        self.width = self.window.width
        self.height = self.window.height
        self.mus: Mus = Mus()
        self.mus.play_music()

    def new_game(self):
        self.snk_x = self.width // self.cell_size // 2 * self.cell_size
        self.snk_y = self.height // self.cell_size // 2 * self.cell_size
        self.snk_dx, self.snk_dy = 0, 0
        self.is_game = True
        self.tail = [(self.snk_x, self.snk_y)]
        self.change_to = None
        self.direction = None
        self.place_food()

    def place_food(self):
        while 1:
            self.fd_x = randint(0, (self.width // self.cell_size) - 1) * self.cell_size
            self.fd_y = randint(0, (self.height // self.cell_size) - 1) * self.cell_size
            if not (self.fd_x, self.fd_y) in self.tail:
                break

    def draw_game_over(self):
        game_over_screen = text.Label(f"Score: {len(self.tail)}\n(Press space to restart)", font_size=24,
                                      x=self.width // 2, y=self.height // 2, width=self.width, align='center',
                                      anchor_x='center', anchor_y='center', multiline=True)
        game_over_screen.draw()

    def check_k(self):
        if any((self.snk_x > self.width or self.snk_x < 0,
                self.snk_y > self.height or self.snk_y < 0)):
            return True

        for num, block in enumerate(self.tail[1:]):
            if (self.snk_x, self.snk_y) == block:
                return True

    def update(self, dt):
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        # Moving the snake
        if self.direction == 'UP':
            self.snk_dy = self.cell_size
            self.snk_dx = 0
        if self.direction == 'DOWN':
            self.snk_dy = -self.cell_size
            self.snk_dx = 0
        if self.direction == 'LEFT':
            self.snk_dx = -self.cell_size
            self.snk_dy = 0
        if self.direction == 'RIGHT':
            self.snk_dx = self.cell_size
            self.snk_dy = 0
        if not self.is_game:
            return

        if self.check_k():
            self.is_game = False
            self.mus.crash.play()
            return

        self.tail.append((self.snk_x, self.snk_y))
        self.snk_x += self.snk_dx
        self.snk_y += self.snk_dy

        if self.snk_x == self.fd_x and self.snk_y == self.fd_y:
            self.place_food()
            self.mus.eat.play()
        else:
            self.tail.pop(0)

    def draw_square(self, x, y, size, colour=(255, 255, 255, 0)):
        self.img = image.create(size, size, image.SolidColorImagePattern(colour))
        self.img.blit(x, y)

    def run(self):
        app.run()
