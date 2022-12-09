from tkinter import Tk, Frame, Label, Button, StringVar

d_frame_cnf = dict(bg='#313131', relief='groove')
d_label_title = dict(fg='white', font=('Calibri', 22, 'bold'))
d_btn_close = dict(fg='white', font=('Calibri', 18, 'bold'), relief='flat')

class FrameHeader(Frame):

    def __init__(self, master, title='', **kw):

        Frame.__init__(self, master, cnf=d_frame_cnf, **kw)
        self.pack(fill='x', expand=True)
        self.__create_title(title=title)
        self.__create_button_close()
        self.callback = None

    def __create_title(self, title):
        lbl_title = Label(master=self, text=title, cnf=d_label_title)
        lbl_title.config(bg=self['bg'])
        lbl_title.pack(side='left')

    def __create_button_close(self):
      btn_close = Button(master=self,text='✖', cnf=d_btn_close)
      btn_close.config(bg = self['bg'], activebackground= self['bg'])
      btn_close['command'] = self.__on_click_close
      btn_close.pack(side='right')

    def set_callback(self,on_click_close):
      self.callback = on_click_close

    # Callbacks

    def __on_click_close(self):
      if self.callback:
        self.callback()

d_frame_cnf = dict(bg='#4D4D4D', relief='groove')
d_btn_lbl = dict(fg='white', font=('Calibri', 18, 'bold'), relief='flat')
d_label = dict(fg='white', font=('Calibri', 18, 'bold'), relief='groove')

class LabeledButton(Frame):
    def __init__(self, master, lbl_txt='Field', btn_txt='B', **kw):
        Frame.__init__(self, master=master, cnf=d_frame_cnf, **kw)

        self.str_var = StringVar(value=lbl_txt)
        label = Label(master=self, textvariable=self.str_var,cnf=d_label)
        label.config(width=10, bg=self['bg'])
        label.pack(side='left', fill='both', expand=True)

        button = Button(master=self, text=btn_txt, width=3, cnf=d_btn_lbl)
        button.config(bg=self['bg'], command=self.__on_click_button)
        button.pack(side='right', fill='y')
        self.callback = None

    def set_callback(self, on_click_button):
        self.callback = on_click_button

    def set_text(self, text):
        self.str_var.set(text)

    def __on_click_button(self):
        if self.callback:
            self.callback()
