from tkinter import Tk, Frame, Label, Button

class States:
    NORMAL = 0
    SELECT = 1

d_frame_cnf = dict(bg='#363636')

d_button_cnf = dict(
    bg='#363636', fg='white', font='Calibri 16 bold', bd=1,
    activebackground='#424242', activeforeground='#EEEDED')

d_btn_styles = {
    States.NORMAL : dict(bg='#363636', relief='raised'),
    States.SELECT : dict(bg='#4E4E4E', relief='sunken'),
    }


class AudioItem(Frame,States):

    # Actions
    CLICK_LABEL = 0
    CLICK_PLAY = 1
    CLICK_DELETE = 2

    def __init__(self, master, _id, text, **kw):
        
        Frame.__init__(self, master, cnf=d_frame_cnf, **kw)
        self._id = _id

        self.btn_label = self.__create_button_label(text)
        self.btn_play = self.__create_button_play()
        self.btn_delete = self.__create_button_delete()
        self.set_state(state=AudioItem.NORMAL)
        self.callback = None

    def __create_button_label(self,text):
        button = Button(master=self, text=text, cnf=d_button_cnf)
        button['command'] = self.__on_click_label
        button.pack(side='left', fill='both', expand=True)
        return button

    def __create_button_play(self):
        button = Button(master=self, text='▶', cnf=d_button_cnf)
        button['command'] = self.__on_click_play
        button.pack(side='left', expand=True)
        return button

    def __create_button_delete(self):
        button = Button(master=self, text='✖', cnf=d_button_cnf)
        button.config(bg = self['bg'], activebackground=self['bg'] , width=10, padx=5 )
        button['command'] = self.__on_click_delete
        button.pack(side='left', fill='both')
        return button

    def __callback(self,action):
        if self.callback:
            if self.callback(action=action, state=self._state, audio_item=self) != False:
                self.set_state(state=AudioItem.SELECT)

    # [ Callbacks ]
    def __on_click_label(self):
        self.__callback(action=AudioItem.CLICK_LABEL)

    def __on_click_play(self):
        self.__callback(action=AudioItem.CLICK_PLAY)

    def __on_click_delete(self):
        self.__callback(action=AudioItem.CLICK_DELETE)

    # [ Methods ]

    def set_callback(self,callback):
        self.callback = callback

    def set_state(self,state):
        self.btn_label.config(d_btn_styles[state])

    def perform_click(self):
        self.btn_label.invoke()

    def get_id(self):
        return self._id

    @property
    def _state(self):
        if self.btn_label['relief'] == 'raised':
            return AudioItem.NORMAL
        else:
            return AudioItem.SELECT
