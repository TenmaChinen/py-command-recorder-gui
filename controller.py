from manager.audio_manager import AudioManager
import numpy as np
import os


class Controller:

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.__init_audio_manager()

    def __init_audio_manager(self):
        self.audio_manager = AudioManager()
        self.audio_manager.set_callback(self.__on_recording)
    
    def __render_group_items(self):
        self.view.clean_all()
        if self.model.has_groups():
            l_groups_id_name = self.model.get_groups_id_name()
            self.view.add_group_items(l_groups_id_name)
            self.view.click_group_item(group_id=self.model.first_group_id)

    def __render_audio_items(self):
        self.view.clean_plot()
        self.view.clean_audio_items()
        self.view.add_audio_items(l_audios_id=self.model.audios_id)
        if self.model.has_audios():
            self.view.click_audio_item(self.model.first_audio_id)

    # [ METHODS ]

    def load_groups_from_path(self,dir_path):
        if dir_path is None:
            dir_path = os.getcwd()
        self.model.set_dir_path(dir_path=dir_path)
        self.model.load_groups_info()
        self.view.set_dir_title(dir_path=dir_path)
        self.__render_group_items()

    def select_group_item(self, group_id):
        if self.model.group_id != group_id:
            self.model.load_group_data(group_id)
            self.__render_audio_items()

    def select_audio_item(self, audio_id):
        title = f'{self.model.group_name} / {audio_id}'
        y_data = self.model.get_audio_data(audio_id)
        self.view.plot_audio(title, y_data)

    def play_audio(self, audio_id):
        y_data = self.model.get_audio_data(audio_id)
        self.audio_manager.load_audio(data=y_data)
        self.audio_manager.play_audio()

    def start_record(self):
        audio = self.audio_manager.record_audio()
        self.model.save_audio(audio)
        self.__render_audio_items()

    def create_new_group(self,group_id):
        self.model.create_new_group(group_id=group_id)
        self.model.load_groups_info()
        # self.model.load_group_data(group_id=group_id)
        self.select_group_item(group_id=group_id)

    def show_delete_dialog(self,item):
        message = f'Are you sure you\nwant to delete :\n{item._id}'
        self.view.dialog_delete.show(message=message,return_data=item)

    # [ CALLBACKS ]

    def on_open_dir(self,dir_path):
        self.load_groups_from_path(dir_path)

    def on_click_add_command(self):
        self.view.add_new_group_item()

    def on_click_button_record(self):
        self.start_record()

    def __on_recording(self):
        state = self.view.btn_record.RECORDING
        self.view.btn_record.set_state(state)

    def on_click_group_item(self,group_id):
        self.select_group_item(group_id)

    def on_click_audio_item(self,audio_id):
        self.select_audio_item(audio_id)

    def on_click_audio_item_play(self,audio_id):
        self.select_audio_item(audio_id)
        self.play_audio(audio_id=audio_id)

    def on_create_new_group(self,group_id):
        self.create_new_group(group_id)

    def on_click_group_item_delete(self,group_item):
        self.show_delete_dialog(item=group_item)
    
    def on_click_delete_audio_item(self, audio_item):
        self.show_delete_dialog(item=audio_item)

    def on_dialog_delete_accept(self,item):
        if self.view.is_group_item(item):
            self.model.delete_group(item._id)
            self.__render_group_items()
            if self.model.has_groups():
                self.view.click_group_item(self.model.first_group_id)
                self.__render_audio_items()
    
        elif self.view.is_audio_item(item):
            self.model.delete_audio(item._id)
            self.__render_audio_items()
            self.model.save_group_data()
