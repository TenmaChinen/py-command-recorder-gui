from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure

class Chart:
    
    def __init__(self, master):
        self.master = master
        self.fig = self.__create_figure()
        self.canvas = self.fig.canvas.get_tk_widget()
        self.__create_plot()
        self.fig.tight_layout()
        # self.fig.subplots_adjust(wspace=0, hspace=0.15, left=0.02, bottom=0.1, right=0.9)
        self.fig.canvas.mpl_connect('resize_event', lambda e : self.fig.tight_layout())

    def __create_figure(self):
        fig = Figure(figsize=(8,5))
        fig_canvas_tk_agg = FigureCanvasTkAgg(figure=fig, master=self.master)
        return fig

    def __create_plot(self):
        self.ax = self.fig.add_subplot(111)
        self.lines, = self.ax.plot([],[], lw=0.4, color='#FFC343')

    def clean(self):
        self.lines.set_data([],[])
        self.ax.set_title('')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.update()

    def set_data(self, title, x_data, y_data):

        self.ax.set_title(title)
        self.lines.set_data(x_data, y_data)

        x_min, x_max = min(x_data), max(x_data)
        y_min, y_max = min(y_data), max(y_data)
        
        y_min, y_max = int(min(y_min,-10000)), int(max(y_max,10000))

        y_delta = y_max-y_min

        y_min = y_min - y_delta * 0.01
        y_max = y_max + y_delta * 0.01

        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)

        self.update()

    def update(self):
        self.fig.canvas.draw_idle()
        self.fig.tight_layout()