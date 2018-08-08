from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from helpers import countdown_solver
from kivy.properties import StringProperty, ListProperty
from kivy.uix.recycleview import RecycleView


class CountdownRoot(BoxLayout):
    goal = StringProperty()
    numbers = StringProperty()
    result = ListProperty()

    def results(self):
        self.result = countdown_solver(int(self.goal), self.numbers.split(","))
        print("Solved")



class CountdownSolverApp(App):
    title = 'Countdown solver'
    icon = 'timer.png'



if __name__ == '__main__':
    CountdownSolverApp().run()