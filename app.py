from kivy.app import App
from kivy.uix.button import Button

class Application(App):
    flag = True
    def build(self):
        return Button(text='Ку',
                      font_size = 30,
                      on_press = self.BNPS_button,
                      background_color = [1, 0, 0, 1],
                      background_normal = '')
    def BNPS_button(self, instance):
        self.flag = not self.flag
        if self.flag: instance.text = 'Ага'
        else: instance.text = 'Нет'

if __name__ == '__main__':
    Application().run()