from tkinter import Tk, Frame, Label, Entry, Button, StringVar

d_entry_bi_state = dict(
    fg='white', relief='raised', justify='center', bd=2,
    font=('Calibri', 18, 'bold'), insertbackground='white')

d_states = dict(
    label = dict( state='readonly', relief='raised', cursor='arrow', readonlybackground='#373737'),
    edit  = dict( state='normal', relief='groove', cursor='xterm', bg='#646464'),
    select  = dict( state='readonly', relief='sunken', cursor='arrow', readonlybackground='#3F3F3F')
    )


class EntryTriState(Entry):

    class Actions:
        LEFT_CLICK = 0
        RIGHT_CLICK = 1
        KEY_ENTER = 2
        FOCUS_OUT = 3

    class States:
        LABEL = 0
        EDIT = 1
        SELECT = 2

    def __init__(self, master, _id, text='' ,**kw):
        self.var = StringVar(value=text)
        Entry.__init__(self, master, textvariable=self.var, cnf=d_entry_bi_state, **kw)
        self._id = _id
        self.bind('<Button-3>', self.__on_click_right)
        self.set_state(state=self.States.LABEL)
        self.callback = None

    def set_callback(self,callback):
        self.callback = callback

    def set_state(self, state):
        if state == self.States.LABEL:
            self.config( **d_states['label'] )
            self.unbind('<FocusOut>')
            self.unbind('<Escape>')
            self.bind('<Button-1>', self.__on_click_left)
        elif state == self.States.EDIT:
            self.config( **d_states['edit'] )
            self.unbind('<Button-1>')
            self.bind('<FocusOut>', self.__on_focus_out)
            self.bind('<Escape>', self.__on_key_press_escape)
            self.bind('<Return>', self.__on_key_press_enter)
            self.focus_set()
            self.selection_range(start=0, end='end')
            self.icursor(index=len(self.var.get()))
        elif state == self.States.SELECT:
            self.config( **d_states['select'] )
            self.unbind('<Button-1>')
            self.unbind('<Escape>')
            self.bind('<FocusOut>', self.__on_focus_out)

    def set_text(self,text):
        self.var.set(value=text)

    def get_text(self):
        return self.var.get()

    def perform_click(self):
        self.focus_set()
        self.__on_click_left(event=None)

    @property
    def _state(self):
        if self['state'] == 'normal':
            return self.States.EDIT
        elif self['relief'] == 'raised':
            return self.States.LABEL
        else:
            return self.States.SELECT

    def __callback(self,action):
        if self.callback:
            return self.callback(action=action, state=self._state, _id=self._id)
        return True

    # [ Callbacks ]

    def __on_focus_out(self,event):
        if self._state in [ self.States.EDIT , self.States.SELECT ]:
            if self.__callback(action=self.Actions.FOCUS_OUT) != False:
                self.set_state(state=self.States.LABEL)

    def __on_click_left(self,event):
        if self.__callback(action=self.Actions.LEFT_CLICK) != False:
            self.set_state(state=self.States.SELECT)
    
    def __on_click_right(self,event):
        if self._state != self.States.EDIT:
            if self.__callback(action=self.Actions.RIGHT_CLICK) != False:
                self.set_state(state=self.States.EDIT)
                self.focus_set()
        elif self._root().focus_get() != self:
            self.focus_set()

    def __on_key_press_escape(self,event):
        if self._state == self.States.EDIT:
            if self.__callback(action=self.Actions.FOCUS_OUT) != False:
                self.set_state(state=self.States.SELECT)

    def __on_key_press_enter(self,event):
        if self._state == self.States.EDIT:
            if self.__callback(action=self.Actions.FOCUS_OUT) != False:
                self.set_state(state=self.States.SELECT)
