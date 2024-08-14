from pyglet import app, clock, window
from pyglet.window import key
from status import StatusWindow
from game import Game
from menu import Menu
from pyglet import resource

SPEED = 10

class GameWindow(window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = Menu(self)
        self.options = None
        self.game = None
        self.state = StatusWindow.MENU
        self.head_image = resource.image("resource/system/snake_head_up.png")
        self.body_image = resource.image("resource/system/snake_body.png")
        self.food = resource.image("resource/system/food.png")

    def start_game(self):
        self.game = Game(self)
        self.state = StatusWindow.GAME
        clock.schedule_interval(self.game.update, 1 / SPEED)
        
    def on_draw(self):
        self.clear()
        if self.state == StatusWindow.MENU:
            self.menu.draw()
        elif self.state == StatusWindow.OPTIONS:
            pass
        elif self.state == StatusWindow.GAME:
            self.game.background_image.blit(0, 0, width=self.game.width, height=self.game.height)
            for num, coord in enumerate(self.game.tail):
                if num == 0:
                    # Обновляем изображение головы змейки в соответствии с текущим направлением
                    head_image = self.game.head_images[self.game.direction]
                    self.game.draw_square(self.game.snk_x, self.game.snk_y, head_image)
                else:
                    self.game.draw_square(coord[0], coord[1], self.body_image)
            self.game.draw_square(self.game.fd_x, self.game.fd_y, self.food)
            if not self.game.is_game:
                self.game.draw_game_over()
            self.game.score_label.draw()

    def on_key_press(self, symbol, modifiers):
        if self.state == StatusWindow.MENU:
            self.menu.on_key_press(symbol, modifiers)
        elif self.state == StatusWindow.OPTIONS:
            pass
        elif self.state == StatusWindow.GAME:
            if self.game.is_game:
                if symbol == key.UP:
                    self.game.change_to = "UP"
                elif symbol == key.DOWN:
                    self.game.change_to = "DOWN"
                elif symbol == key.LEFT:
                    self.game.change_to = 'LEFT'
                elif symbol == key.RIGHT:
                    self.game.change_to = "RIGHT"
                elif symbol == key.ESCAPE:
                    self.return_to_menu()
            else:
                if symbol == key.SPACE:
                    self.game.new_game()
                elif symbol == key.ESCAPE:
                    self.return_to_menu()

    def return_to_menu(self):
        clock.unschedule(self.game.update)
        self.state = StatusWindow.MENU 
        self.game = None  