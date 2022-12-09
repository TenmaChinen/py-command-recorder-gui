from components.buttons import ButtonNormal, ButtonRecord
from components.scroll_frame import ScrollFrame
from components.frames import LabeledButton
from components.dialogs import DialogDelete
from components.group_item import GroupItem
from components.audio_item import AudioItem
from tkinter import Tk, Frame, filedialog
from components.labels import LabelTitle
from components.chart import Chart
import os

class View:

    def __init__(self):
        self.root = self.__create_root()
        self.chart = self.__create_chart()
        self.fr_right = self.__create_frame_right()
        self.lbl_btn_dir = self.__create_labeled_button_dir()
        self.fr_groups = self.__create_frame_groups()
        self.fr_audios = self.__create_frame_audios()
        self.sfr_groups = self.__create_scroll_frame_groups()
        self.sfr_audios = self.__create_scroll_frame_audios()
        self.btn_record = self.__create_button_record()
        self.btn_add_cmd =self.__create_button_add_command()
        self.dialog_delete = self.__create_dialog_delete()
        self.root.update()

    def __create_root(self):
        root = Tk()
        # root.geometry('200x400+100+100')
        root.configure(bg='#363636')
        root.bind_all('<Control-q>', lambda event: root.destroy())
        return root

    def __create_chart(self):
        chart = Chart(master=self.root)
        chart.canvas.pack(side='left', fill='both')
        return chart

    def __create_frame_right(self):
        fr_right = Frame(master=self.root)
        fr_right.pack(side='right',fill='both', expand=True)
        fr_right.grid_columnconfigure(0,weight=1, pad=60)
        fr_right.grid_columnconfigure(1,weight=1, pad=20)
        fr_right.grid_rowconfigure(0,weight=1, uniform='row')
        fr_right.grid_rowconfigure(1,weight=9, uniform='row')
        return fr_right

    def __create_labeled_button_dir(self):
        labeled_button = LabeledButton(master=self.fr_right, lbl_txt='Directory', btn_txt='📁')
        labeled_button.set_callback(on_click_button=self.__on_click_btn_open_dir)
        labeled_button.grid(row=0, column=0, columnspan=2, sticky='news')
        return labeled_button

    def __create_frame_groups(self):
        fr_groups = Frame(master=self.fr_right, bg=self.root['bg'])
        fr_groups.grid(row=1, column=0, sticky='news')

        lbl_group = LabelTitle(master=fr_groups,text='GROUPS')
        lbl_group.pack(side='top', fill='x')

        return fr_groups

    def __create_frame_audios(self):
        fr_audios = Frame(master=self.fr_right, bg=self.root['bg'])
        fr_audios.grid(row=1, column=1, sticky='news')

        lbl_audios = LabelTitle(master=fr_audios,text='AUDIO')
        lbl_audios.pack(side='top', fill='x')

        return fr_audios

    def __create_scroll_frame_groups(self):
        sfr_groups = ScrollFrame(master=self.fr_groups, width=200)
        sfr_groups.pack(side='top', fill='both', expand=True)
        sfr_groups.set_bg('#353535')
        sfr_groups.last_widget = None
        return sfr_groups

    def __create_scroll_frame_audios(self):
        sfr_audios = ScrollFrame(master=self.fr_audios, width=250)
        sfr_audios.pack(side='top', fill='both', expand=True)
        sfr_audios.set_bg('#353535')
        self.last_audio_item_id = None
        return sfr_audios

    def __create_button_add_command(self):
        button_add_command = ButtonNormal(master=self.fr_groups, text='ADD COMMAND')
        button_add_command['command'] = self.__on_click_add_command
        button_add_command.pack(side='bottom', fill='x', expand=False)
        return button_add_command

    def __create_button_record(self):
        button_record = ButtonRecord(master=self.fr_audios)
        button_record.pack(side='bottom', fill='x', expand=False)
        button_record.set_callback(self.__on_click_record)
        return button_record

    def __create_dialog_delete(self):
        dialog_delete = DialogDelete(master=self.root)
        dialog_delete.set_callback(self.__on_dialog_delete_accept)
        return dialog_delete

    # [ METHODS ]

    def set_controller(self, controller):
        self.controller = controller

    def add_group_item(self, group_id, group_name):
        group_item = GroupItem(master=self.sfr_groups.frame, _id=group_id, text=group_name)
        group_item.set_callback(callback=self.__on_click_group_item)
        group_item.pack(side='top')

    def add_audio_item(self, _id, name):
        audio_item = AudioItem(master=self.sfr_audios.frame, _id=_id, text=name)
        audio_item.set_callback(self.__on_click_audio_item)
        audio_item.pack(side='top',fill='x', expand=True)

    def add_group_items(self, l_groups_id_name):        
        for group_id, group_name in l_groups_id_name:
            self.add_group_item(group_id = group_id, group_name=group_name)

    def add_audio_items(self, l_audios_id):
        for audio_id in l_audios_id:
            self.add_audio_item(_id=audio_id, name=audio_id)
        self.sfr_audios.last_audio_item_id = None

    def add_new_group_item(self):
        group_item = GroupItem(master=self.sfr_groups.frame, _id=None, text='New Command')
        group_item.set_callback(callback=self.__on_click_group_item)
        group_item.set_state(state=GroupItem.States.EDIT)
        group_item.pack(side='top')

    def set_dir_title(self,dir_path):
        dir_path = dir_path.replace('\\','/')
        dir_title = '/'.join(dir_path.split('/')[-2:])
        print(dir_title)
        self.lbl_btn_dir.set_text(text=dir_title)

    def plot_audio(self, title, y_data):
        x_data = range(y_data.size)
        self.chart.set_data(title, x_data, y_data)

    def clean_group_items(self):
        self.sfr_groups.remove_children()
        self.sfr_groups.update()

    def clean_audio_items(self):
        self.last_audio_item_id = None
        self.sfr_audios.remove_children()
        self.sfr_audios.set_scroll_y(fraction=0)
        self.sfr_audios.update()

    def clean_plot(self):
        self.chart.clean()

    def clean_all(self):
        self.clean_group_items()
        self.clean_audio_items()
        self.clean_plot()

    def get_widget(self, master, _id):
        for widget in master.winfo_children():
            if widget._id == _id:
                return widget
    
    def get_group_item(self, group_id):
        return self.get_widget(master=self.sfr_groups.frame, _id=group_id)

    def get_audio_item(self, audio_id):
        return self.get_widget(master=self.sfr_audios.frame, _id=audio_id)

    def click_group_item(self, group_id):
        group_item = self.get_group_item(group_id=group_id)
        if group_item:
            group_item.perform_click()

    def click_audio_item(self, audio_id):
        audio_item = self.get_audio_item(audio_id=audio_id)
        if audio_item:
            audio_item.perform_click()

    def is_group_item(self,item):
        return isinstance(item, GroupItem)

    def is_audio_item(self,item):
        return isinstance(item, AudioItem)

    # [ CALLBACKS ]

    def __on_click_group_item(self, action, state, group_item):
        group_id = group_item.get_id()
        if action == GroupItem.Actions.DELETE:
            self.controller.on_click_group_item_delete(group_item)
        elif state == GroupItem.States.LABEL:
            if action == GroupItem.Actions.LEFT_CLICK:
                self.controller.on_click_group_item(group_id = group_id)
            elif action == GroupItem.Actions.RIGHT_CLICK:
                self.controller.on_click_group_item(group_id = group_id)
        elif state == GroupItem.States.EDIT:
            if group_item.get_text() == '':
                # TODO : Show Toast warning user that cannot be empty ( maybe integrate in widget )
                return False
            if action == GroupItem.Actions.FOCUS_OUT:
                if group_id is None:
                    new_group_id = group_item.get_text().lower().replace(' ','_')
                    group_item.set_id(_id=new_group_id)
                    self.controller.on_create_new_group(new_group_id)


    def __on_click_audio_item(self, action, state, audio_item):
        audio_id = audio_item.get_id()
        if action == AudioItem.CLICK_LABEL:
            self.controller.on_click_audio_item(audio_id=audio_id)
        elif action == AudioItem.CLICK_PLAY:
            self.controller.on_click_audio_item_play(audio_id=audio_id)
        elif action == AudioItem.CLICK_DELETE:
            self.controller.on_click_delete_audio_item(audio_item=audio_item)

        if self.last_audio_item_id:
            audio_item = self.get_audio_item(audio_id=self.last_audio_item_id)
            audio_item.set_state(AudioItem.NORMAL)
        self.last_audio_item_id = audio_id

    def __on_click_add_command(self):
        self.controller.on_click_add_command()

    def __on_click_record(self):
        self.controller.on_click_button_record()

    def __on_dialog_delete_accept(self,audio_id):
        self.controller.on_dialog_delete_accept(audio_id)
       
    def __on_click_btn_open_dir(self):
        l_file_types = [('Numpy Compress Format', '*.npz')]
        dir_path = filedialog.askdirectory(title='Open Command Audios Directory', initialdir=os.getcwd())
        self.controller.on_open_dir(dir_path) 