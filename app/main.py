from gameWindow import GameWindow, app


if __name__ == '__main__':
    game_window = GameWindow(1920, 1080, "Game Menu", resizable=False, fullscreen=True)
    
    app.run()