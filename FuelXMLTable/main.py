from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class FuelRoot(BoxLayout):
    pass


class FuelApp(App):
    FuelRoot()


if __name__ == '__main__':
    FuelApp().run()