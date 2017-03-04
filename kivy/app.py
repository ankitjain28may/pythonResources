from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
# from kivy.graphics import Color, Ellipse, Line
from kivy.config import Config

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '250')

class MyDesktopApp(App):
    def build(self):
        root = Widget()
        b1 = Button(pos=(0, 0),
                    # background_color=(226, 13, 13, 1),
                    size=(100, 50),
                    text="Click Me")
        root.add_widget(b1)
        return root

if __name__ == '__main__':
    MyDesktopApp().run()