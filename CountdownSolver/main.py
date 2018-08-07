from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from helpers import countdown_solver
from kivy.properties import ListProperty, NumericProperty

class CountdownRoot(BoxLayout):
    pass


class CountdownSolverApp(App):
    title = 'Countdown solver'
    icon = 'timer.png'


if __name__ == '__main__':
    CountdownSolverApp().run()