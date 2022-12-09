from tkinter import Tk, Frame, Canvas, Label, Scrollbar, Button


class ScrollFrame(Frame):
    def __init__(self, master, cnf={}, **kw):
        Frame.__init__(self, master, cnf=cnf, **kw)
        self.canvas = self.__create_canvas()
        self.scrollbar = self.__create_scrollbar()
        self.frame = self.__create_frame()
        self.canvas.pack(side='left', fill='both', expand=True)
        self.__setup_listeners()
        self.pack_propagate(flag=False)

    def __create_canvas(self):
        canvas = Canvas(master=self, bg='red')
        canvas.config(highlightthickness=0)
        # canvas.pack_propagate(flag=False)
        return canvas

    def __create_scrollbar(self):
        scrollbar = Scrollbar(self, orient='vertical',command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        return scrollbar

    def __create_frame(self):
        frame = Frame(self.canvas, bg='darkblue')
        frame.cid = self.canvas.create_window((0, 0), window=frame, anchor='nw')
        return frame

    def __setup_listeners(self):
        self.frame.bind('<Configure>', self.__on_frame_scroll_change)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.__on_canvas_size_change)
        self.canvas.bind_all('<MouseWheel>', self.__on_scroll_mouse)

    def __on_canvas_size_change(self,event):
        # print('Canvas Size Change : ')
        self.canvas.itemconfig(self.frame.cid, width=event.width)

    def __on_frame_scroll_change(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        l_canvas_bbox = list(self.canvas.bbox('all'))

        if event.height < canvas_height:
            l_canvas_bbox[3] = canvas_height
        
        self.canvas.configure(scrollregion=l_canvas_bbox)

    def __on_scroll_mouse(self, event):
        self.canvas.yview_scroll(- 1 * int(event.delta / 120), 'units')

    def set_bg(self,bg):
        self.canvas.config(bg=bg)
        self.frame.config(bg=bg)

    def remove_children(self):
        for child in self.frame.winfo_children():
            child.destroy()

    def get_children(self):
        return self.frame.winfo_children()

    def set_scroll_y(self,fraction):
        self.canvas.yview_moveto(fraction)