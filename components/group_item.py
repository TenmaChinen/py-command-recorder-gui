from .entries import EntryTriState
from tkinter import Frame, Button

d_frame = dict()
d_btn_delete = dict(bg='#373737', fg='white', font=('Calibri', 16, 'bold'), relief='raised')

class GroupItem(Frame):
        
    class States(EntryTriState.States):
        pass

    class Actions(EntryTriState.Actions):
        DELETE = 4

    def __init__(self, master, _id, text='Field' ,**kw):
        self._id = _id
        Frame.__init__(self, master, cnf=d_frame, **kw)
        self.callback = None
        self.et_tri = self.__create_entry_tristate(text)
        self.btn_del = self.__create_button_delete()

    def __create_entry_tristate(self,text):
        entry_tri_state = EntryTriState(master=self, _id=self._id, text=text, width=16)
        entry_tri_state.set_callback(callback=self.__entry_tristate_callback)
        entry_tri_state.pack(side='left', fill='both', expand=True)
        return entry_tri_state

    def __create_button_delete(self):
      btn_delete = Button(master=self,text='✖', cnf=d_btn_delete, width=3)
      btn_delete.config(activebackground= self['bg'])
      btn_delete['command'] = self.__on_click_delete
      btn_delete.pack(side='left', expand=True)
      return btn_delete

    # [ Methods ]

    def set_callback(self,callback):
        self.callback = callback

    def get_id(self):
        return self._id

    def set_id(self,_id):
        self._id = _id

    def get_text(self):
        return self.et_tri.get_text()
    
    def set_text(self,text):
        self.et_tri.set_text(text)

    def set_state(self,state):
        self.et_tri.set_state(state=state)

    def perform_click(self):
        self.et_tri.perform_click()

    # [ Callbacks ]

    def __entry_tristate_callback(self,action,state,_id):
        if self.callback:
            return self.callback(action=action,state=state, group_item=self)

    def __on_click_delete(self):
        if self.callback:
            state = self.et_tri._state
            return self.callback(action=self.Actions.DELETE,state=state, group_item=self)