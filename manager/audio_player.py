from pyaudio import PyAudio, paInt16
from threading import Thread
from io import BytesIO
from time import sleep
import struct
import wave

RATE = 16000
CHUNK_SIZE = 1024 * 2

class AudioPlayer:

    def __init__(self, py_audio):
        self.py_audio = py_audio
        self.buffer_io = None
        self.stream = None
        self.open_stream()

    def open_stream(self):
        if self.stream:
            return False
            
        self.stream = self.py_audio.open(format=paInt16, channels=1, rate=RATE, output=True, start=False)
    
    def close_stream(self):
        if self.stream:
            self.stream.close()
            self.stream = None

    def start_stream(self):
        if self.stream and self.stream.is_stopped():
            self.stream.start_stream()
    
    def stop_stream(self):
        if self.stream and self.stream.is_playing():
            self.stream.stop_stream()

    def load_audio(self,data):
        self.buffer_io = BytesIO(struct.pack('h'*data.size, *data))

    def play(self):
        if self.buffer_io is None:
            return False
        
        if self.stream is None:
            self.open_stream()

        self.is_playing = False
        
        while self.stream.is_active():
            sleep(0.1)

        thread = Thread(target=self.callback, args=())
        thread.start()

    def is_active(self):
        return self.stream and self.stream.is_active()

    def callback(self):
        self.buffer_io.seek(0)
        data = self.buffer_io.read(CHUNK_SIZE)
        self.stream.start_stream()
        self.is_playing = True
        while self.is_playing and data != b'':
            self.stream.write(data)
            data = self.buffer_io.read(CHUNK_SIZE)
        
        self.stream.stop_stream()


