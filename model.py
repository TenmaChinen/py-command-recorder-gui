from datetime import datetime
import numpy as np
import os

class Model:
    
    def __init__(self):

        self.dir_path = None
        self.d_groups_info = None
        self.d_group = None

    # def load_first_group(self):
    #     if self.d_groups_info:
    #         self.load_group_data(group_id=self.first_group_id)

    def __get_group_data(self,group_id):
        file_name = self.d_groups_info[group_id]['file_name']
        file_path = f'{self.dir_path}/{file_name}'
        d_group_data = dict(np.load(file_path))
        return d_group_data

    # Methods

    def set_dir_path(self,dir_path):
        self.dir_path = dir_path
    
    def load_groups_info(self):
        d_groups_info = {}
        if self.dir_path:
            for file_name in os.listdir(self.dir_path)[::-1]:
                if file_name.endswith('.npz'):
                    group_id = file_name[0:-4]
                    group_name = group_id.upper().replace('_', ' ')
                    d_groups_info[group_id] = dict( name = group_name, file_name = file_name )
            self.d_groups_info = d_groups_info

    def load_group_data(self, group_id):
        d_group_data = self.__get_group_data(group_id)
        group_name = self.d_groups_info[group_id]['name']
        self.d_group = dict( id = group_id, name=group_name ,data = d_group_data )

    def save_group_data(self):
        file_name = self.d_groups_info[self.group_id]['file_name']
        np.savez(f'{self.dir_path}/{file_name}', **self.group_data)

    def save_audio(self,audio):
        new_id = generate_id()
        self.group_data[new_id] = audio
        self.save_group_data()

    def delete_group(self,group_id):
        file_name = self.d_groups_info[group_id]['file_name']
        file_path = f'{self.dir_path}/{file_name}'
        os.remove(path=file_path)
        del self.d_groups_info[group_id]


    def delete_audio(self,audio_id):
        del self.group_data[audio_id]

    #

    def has_groups(self):
        return self.d_groups_info and len(self.d_groups_info) != 0

    def has_audios(self):
        return len(self.group_data) != 0

    def get_audio_data(self,audio_id):
        return self.group_data[audio_id]

    def get_groups_id_name(self):
        if self.d_groups_info:
            return [ [k,d['name']] for k,d in self.d_groups_info.items()]

    def create_new_group(self,group_id):
        save_path = f'{self.dir_path}/{group_id}'
        np.savez(file=save_path)

    @property
    def groups_id(self):
        return list(self.d_groups_info.keys())

    @property
    def first_group_id(self):
        return self.groups_id[0]

    @property
    def groups_name(self):
        return [ d['name'] for d in self.d_groups_info.values()]

    @property
    def group_id(self):
        if self.d_group:
            return self.d_group['id']

    @property
    def group_name(self):
        return self.d_group['name']

    @property
    def group_data(self):
        return self.d_group['data']

    @property
    def audios_id(self):
        l_audios_id = list(self.group_data.keys())
        l_audios_id.reverse()
        return l_audios_id

    @property
    def first_audio_id(self):
        l_audios_id = self.audios_id
        if l_audios_id:
            return self.audios_id[0]
        return None



def generate_id():
    new_id = datetime.now().strftime('%d%m%y-%H%M%S-%f')
    return new_id[0:-4] 