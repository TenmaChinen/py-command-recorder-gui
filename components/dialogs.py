from tkinter import Tk, Frame, Label, Button, StringVar
from .frames import FrameHeader

d_frame_cnf = dict(bg='#414141', bd=2)
d_lbl_message = dict(fg='white', font=('Calibri',16,'bold'), padx=15, pady=20)
d_btn_dialog = dict(fg='white', font=('Calibri',16,'bold'), relief='flat')
d_fr_footer_cnf = dict(bg='#313131', bd=1)

class DialogDelete(Frame):

    ACCEPT = 0
    CANCEL = 1

    def __init__(self, master, **kw):
        
        Frame.__init__(self, master, cnf=d_frame_cnf, **kw)
        self.__create_frame_header()
        self.var_message = self.__create_label_message()
        self.fr_footer = self.__create_frame_footer()
        self.__create_button_cancel()
        self.__create_button_accept()
        self.__return_data = None
        self.__callback = None

    def __create_frame_header(self):
        fr_header = FrameHeader(master=self, title='Delete')
        fr_header.set_callback(on_click_close=self.__on_click_close)
        fr_header.pack(side='top')

    def __create_label_message(self):
        var_message = StringVar()
        lbl_message = Label(master=self,textvariable=var_message, cnf=d_lbl_message)
        lbl_message.config(bg=self['bg'], width=20)
        lbl_message.pack(side='top', fill='both', expand=True)
        return var_message

    def __create_frame_footer(self):
        fr_footer = Frame(master=self, cnf=d_fr_footer_cnf)
        fr_footer.pack(side='bottom', fill='x', expand=True)
        return fr_footer

    def __create_button_cancel(self):
        btn_cancel = Button(master=self.fr_footer, text='Cancel', cnf=d_btn_dialog)
        btn_cancel['command'] = self.__on_click_cancel
        btn_cancel.config(bg=self.fr_footer['bg'], activebackground=self.fr_footer['bg'])
        btn_cancel.pack(side='right')
    
    def __create_button_accept(self):
        btn_accept = Button(master=self.fr_footer, text='Accept', cnf=d_btn_dialog)
        btn_accept['command'] = self.__on_click_accept
        btn_accept.config(bg=self.fr_footer['bg'], activebackground=self.fr_footer['bg'])
        btn_accept.pack(side='right')

    # Callbacks

    def __on_click_close(self):
        self.hide()

    def __on_click_accept(self):
        self.hide()
        if self.__callback:
            self.__callback(self.__return_data)

    def __on_click_cancel(self):
        self.hide()

    # Methods

    def set_callback(self,on_click_accept):
        self.__callback = on_click_accept

    def set_message(self,message):
        self.var_message.set(message)

    def show(self,message=None,return_data=None):
        self.__return_data = return_data
        if message is not None:
            self.var_message.set(message)

        self.place(relx=0.5, rely=0.5, anchor='center')

    def hide(self):
        self.place_forget()

