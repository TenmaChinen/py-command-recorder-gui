from pyaudio import PyAudio, paInt16
import numpy as np
from time import sleep

RATE = 16000

class AudioRecorder:

    def __init__(self, py_audio, record_seconds=2):
        self.py_audio = py_audio
        self.__set_length(record_seconds)
        self.stream = None
        self.open_stream()
        self.on_recording = None

    def __set_length(self,record_seconds):
        self.length = int(RATE * record_seconds)

    def __wait_threshold(self):
        while True:
            value = abs(int.from_bytes(self.stream.read(1), 'little', signed=True))
            if value > 1000:
                break

    def __trim_audio(self,audio):
        length = audio.size
        for idx in range(length-1, -1,-1):
            value = abs(audio[idx])
            if value > 2000:
                idx_end = min(length,idx+1000)
                return audio[0:idx_end]

        return audio
        

    def open_stream(self):
        if self.stream:
            return False
        self.stream = self.py_audio.open(format=paInt16, channels=1, rate=RATE, frames_per_buffer = 1, input=True)
        self.stream.stop_stream()

    def close_stream(self):
        if self.stream:
            self.stream.close()
            self.stream = None
    
    def start_stream(self):
        if self.stream and self.stream.is_stopped():
            self.stream.start_stream()
    
    def stop_stream(self):
        if self.stream and self.stream.is_active():
            self.stream.stop_stream()

    def record(self):
        if self.stream is None:
            self.open_stream()

        self.stream.start_stream()
        self.__wait_threshold()
        self.__is_recording()

        l_frames = [ self.stream.read(1) for _ in range(0, self.length) ]
        self.stream.stop_stream()
        audio = np.frombuffer(b''.join(l_frames), dtype=np.int16)
        
        audio = self.__trim_audio(audio)
        return audio

    def is_active(self):
        return self.stream and self.stream.is_active()

    def set_callback(self,on_recording):
        self.on_recording = on_recording

    # Callbacks

    def __is_recording(self):
        if self.on_recording:
            self.on_recording()
