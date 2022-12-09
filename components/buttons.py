from tkinter import Tk, Button

d_btn_normal = dict(bg='#363636', fg='white', font='Calibri 16 bold', activebackground='#505050', activeforeground='#EEEDED', bd=1)
d_btn_group = dict(bg='#363636', fg='white', font='Calibri 16 bold', activebackground='#505050', activeforeground='#EEEDED', bd=1)
d_btn_record = dict(bg='#363636', fg='white', font='Calibri 16 bold', activebackground='#505050', activeforeground='#EEEDED', bd=1)

class ButtonNormal(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master, cnf=d_btn_normal, **kw)
        self.pack(fill='x', expand=True)

class ButtonGroup(Button):

    def __init__(self, master, _id, **kw):
        Button.__init__(self, master, cnf=d_btn_group, **kw)
        self._id = _id
        self['command'] = self.__on_click
        self.pack(fill='x', expand=True)
        self.callback = None

    def set_active(self,state):
        self['relief'] = 'sunken' if state else 'raised'
        if self['relief'] == 'sunken':
            self['bg'] = d_btn_group['activebackground']
        else:
            self['bg'] = d_btn_group['bg']

    def set_callback(self,callback):
        self.callback = callback

    def __on_click(self):
        if self.callback:
            self.callback(self._id)


class ButtonRecord(Button):

    NORMAL = 0
    LISTENING = 1
    RECORDING = 2

    d_texts = { NORMAL : '🎤', LISTENING : 'Say something', RECORDING : 'Recording...' }

    def __init__(self, master, **kw):
        Button.__init__(self, master, cnf=d_btn_record, **kw)
        self.config(command=self.__on_click)
        # self.pack(fill='x', expand=True)
        self.set_state(self.NORMAL)
        self.callback = None

    def set_callback(self,callback):
        self.callback = callback

    def set_state(self,state):
        self['text'] = self.d_texts[state]
        self.update()

    def __on_click(self):
        if self.callback:
            self.set_state(self.LISTENING)
            self.callback()
            self.set_state(self.NORMAL)

