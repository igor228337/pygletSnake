from pyglet import app, window
from pyglet.text import Label
from pyglet.window import key


class Menu:
    def __init__(self, window: window.Window):
        self.window = window
        self.selected_index = 0
        self.items = ["Start Game", "Exit"]
        self.labels = []
        self.create_labels()

    def create_labels(self):
        y = self.window.height // 2 + 50
        for item in self.items:
            label = Label(item, font_name='Arial', font_size=36,
                          x=self.window.width // 2, y=y,
                          anchor_x='center', anchor_y='center')
            self.labels.append(label)
            y -= 50

    def draw(self):
        for i, label in enumerate(self.labels):
            if i == self.selected_index:
                label.color = (255, 0, 0, 255)
            else:
                label.color = (255, 255, 255, 255)
            label.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.items)
        elif symbol == key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.items)
        elif symbol == key.ENTER:
            self.select_item()

    def select_item(self):
        selected_item = self.items[self.selected_index]
        if selected_item == "Start Game":
            self.window.start_game()
        elif selected_item == "Options":
            print("Opening options...")
        elif selected_item == "Exit":
            app.exit()