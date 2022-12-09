from controller import Controller
from model import Model
from view import View

class App:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.controller = Controller(self.view, self.model)
        self.view.set_controller(self.controller)

    def run(self):
        self.view.root.mainloop()

if __name__ == '__main__' :
    app = App()
    
    # path = r'C:/Users/tenma/Data Drive/speech/new'
    # path = r'C:/Users/tenma/Code Drive/01. C O D E/00. Python/20. T O O L S/07. Peripherials/commands_recorder_gui/assets/audios'
    # app.controller.load_groups_from_path(dir_path=path)
    app.controller.load_groups_from_path(dir_path=None)

    app.run()