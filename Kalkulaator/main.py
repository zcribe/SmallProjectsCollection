from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class CalculatorRoot(BoxLayout):
    expression = StringProperty()

    def _evaluate(self, expression):
        try:
            self.expression = str(eval(expression))
        except:
            self.expression = "Error"


class CalculatorApp(App):
    title = "Kalkulaator"
    icon = "kalkulaator.png"


if __name__ == '__main__':
    CalculatorApp().run()