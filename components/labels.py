from tkinter import Tk, Label

d_label_title = dict(font='Arial 20 bold', fg='white', relief='ridge')

class LabelTitle(Label):

    def __init__(self, master, **kw):
        Label.__init__(self, master, cnf=d_label_title, **kw)
        self.config(bg=master['bg'])