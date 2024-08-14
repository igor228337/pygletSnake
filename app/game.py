from pyglet.window import Window
from random import randint
from pyglet import text, resource, sprite
from mus import Mus
from pyglet import app
from config import logger

class Game:
    body_image = resource.image("resource/system/snake_body.png")
    CELL_SIZE = body_image.width
    head_images = {
            'UP': resource.image("resource/system/snake_head_up.png"),
            'DOWN': resource.image("resource/system/snake_head_down.png"),
            'LEFT': resource.image("resource/system/snake_head_left.png"),
            'RIGHT': resource.image("resource/system/snake_head_right.png")
        }
    def __init__(self, window: Window):
        self.food = resource.image("resource/system/food.png")
        self.window = window
        self.width = self.window.width
        self.height = self.window.height
        self.mus = Mus()
        self.background_image = resource.image("resource/system/snake.jpg")
        self.score = 0  
        self.score_label = text.Label(f'Счёт: {self.score}', font_size=36,
                                      x=self.width - 100, y=self.height - 30,
                                      anchor_x='right', anchor_y='top')
        self.new_game()
        

    def new_game(self):
        self.mus.play_music()
        self.snk_x = self.width // self.CELL_SIZE // 2 * self.CELL_SIZE
        self.snk_y = self.height // self.CELL_SIZE // 2 * self.CELL_SIZE
        self.snk_dx, self.snk_dy = 0, 0
        self.is_game = True
        self.tail = [(self.snk_x, self.snk_y)]
        self.change_to = None
        self.direction = "UP"
        self.score = 0 
        self.score_label.text = f'Счёт: {self.score}' 
        self.place_food()

    def place_food(self):
        while True:
            self.fd_x = randint(0, (self.width // self.CELL_SIZE) - 1) * self.CELL_SIZE
            self.fd_y = randint(0, (self.height // self.CELL_SIZE) - 1) * self.CELL_SIZE
            if (self.fd_x, self.fd_y) not in self.tail:
                break

    def draw_game_over(self):
        self.mus.close_music()
        game_over_text = f"Счёт: {len(self.tail)}\n(Нажмите пробел для перезапуска)"
        game_over_screen = text.Label(game_over_text, font_size=36,
                                      x=self.width // 2, y=self.height // 2, width=self.width, align='center',
                                      anchor_x='center', anchor_y='center', multiline=True)
        game_over_screen.draw()

    def check_collision(self):
        if self.snk_x < 0 or self.snk_x >= self.width or self.snk_y < 0 or self.snk_y >= self.height:
            return True
        for block in self.tail[1:]:
            if (self.snk_x, self.snk_y) == block:
                return True
        return False

    def update(self, dt):
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.snk_dy = self.CELL_SIZE
            self.snk_dx = 0
        if self.direction == 'DOWN':
            self.snk_dy = -self.CELL_SIZE
            self.snk_dx = 0
        if self.direction == 'LEFT':
            self.snk_dx = -self.CELL_SIZE
            self.snk_dy = 0
        if self.direction == 'RIGHT':
            self.snk_dx = self.CELL_SIZE
            self.snk_dy = 0

        if not self.is_game:
            return

        if self.check_collision():
            self.is_game = False
            self.mus.crash.play()
            return

        self.tail.append((self.snk_x, self.snk_y))
        self.snk_x += self.snk_dx
        self.snk_y += self.snk_dy

        if self.snk_x == self.fd_x and self.snk_y == self.fd_y:
            self.place_food()
            self.mus.eat.play()
            self.score += 1 
            self.score_label.text = f'Счёт: {self.score}' 
        else:
            self.tail.pop(0)

    def draw_square(self, x, y, sprite_image):
        sprite_obj = sprite.Sprite(sprite_image, x=x, y=y)
        sprite_obj.draw()

    def draw(self):
        self.background_image.blit(0, 0, width=self.width, height=self.height)

        head_image = self.head_images[self.direction]
        logger.info(self.direction)
        logger.info(head_image)
        self.draw_square(self.snk_x, self.snk_y, head_image)

        for segment in self.tail[1:]:
            self.draw_square(segment[0], segment[1], self.body_image)

        self.draw_square(self.fd_x, self.fd_y, self.food)

        if not self.is_game:
            self.draw_game_over()
            
        self.score_label.draw()

    def run(self):
        app.run()