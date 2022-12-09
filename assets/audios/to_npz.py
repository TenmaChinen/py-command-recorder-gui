from datetime import datetime
from time import sleep
import numpy as np
import os

def get_id():
	new_id = datetime.now().strftime('%d%m%y-%H%M%S-%f')
	return new_id[0:-4] 

for file_name in os.listdir():
	if not file_name.endswith('.npy'): continue
	file_name = file_name[0:-4]
	file_path = f'{file_name}.npy'
	data = np.load(file_path).astype(np.int16)
	d_data = {}
	print(file_name)
	for audio in data:
		new_id = get_id()
		d_data[new_id] = audio
		# print(file_name,new_id)
		sleep(0.002)
	
	save_path = f'{file_name}.npz'
	np.savez(save_path, **d_data)