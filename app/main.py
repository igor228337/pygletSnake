from pyglet.window import key
from game import Game
from pyglet import clock


app_window: Game = Game()
window = app_window.window


@window.event
def on_draw():
    window.clear()
    for num, coord in enumerate(app_window.tail):
        if num == 0:
            app_window.draw_square(app_window.snk_x, app_window.snk_y, app_window.cell_size)
        else:
            app_window.draw_square(coord[0], coord[1], app_window.cell_size, colour=(127, 127, 127, 0))
    app_window.draw_square(app_window.fd_x, app_window.fd_y, app_window.cell_size, colour=(255, 0, 0, 0))
    if not app_window.is_game:
        app_window.draw_game_over()


@window.event
def on_key_press(symbol, modifiers):
    if app_window.is_game:
        if symbol == key.UP:
            app_window.change_to = "UP"
        elif symbol == key.DOWN:
            app_window.change_to = "DOWN"
        elif symbol == key.LEFT:
            app_window.change_to = 'LEFT'
        elif symbol == key.RIGHT:
            app_window.change_to = "RIGHT"
    else:
        if symbol == key.SPACE:
            app_window.new_game()


if __name__ == '__main__':
    app_window.new_game()
    app_window.place_food()
    clock.schedule_interval(app_window.update, 1 / 30)
    app_window.run()
