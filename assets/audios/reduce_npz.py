from datetime import datetime
from time import sleep
import numpy as np
import os

for file_name in os.listdir():

    if not file_name.endswith('.npz') or file_name == 'ruidos.npz':
        continue

    print(file_name)

    file_path = f'{file_name}'
    data = np.load(file_path)
    d_data = {}
    
    for key in data.keys():
        audio = data[key]
        if audio.min() < 4000 or audio.max() > 4000:
            length = audio.size
            for idx in range(length-1, -1, -1):
                value = audio[idx]
                if value < -2000 or value > 2000:
                    break
            else:
                continue
            idx = min(idx+1000, length)
            d_data[key] = audio[0:idx]
    
    np.savez(file_path,**d_data)
