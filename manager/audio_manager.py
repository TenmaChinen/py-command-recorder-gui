from .audio_recorder import AudioRecorder
from .audio_player import AudioPlayer
from pyaudio import PyAudio

class AudioManager:

    def __init__(self):
        self.__py_audio = PyAudio()
        self.__audio_player = AudioPlayer(self.__py_audio) 
        self.__audio_recorder = AudioRecorder(self.__py_audio)
        self.__audio_recorder.set_callback(self.__on_recording)
        self.callback = None

    def terminate(self):
        self.__py_audio.terminate()

    # Recorder
    def record_audio(self):
        # if not self.__audio_recorder.is_active():
            # self.init_audio_recorder()
        return self.__audio_recorder.record()

    def init_audio_recorder(self):
        self.__audio_player.close_stream()
        self.__audio_recorder.open_stream()

    # Player
    def load_audio(self,data):
        self.__audio_player.load_audio(data)

    def play_audio(self):
        # if not self.__audio_player.is_active():
            # self.init_audio_player()

        self.__audio_player.play()

    def init_audio_player(self):
        self.__audio_recorder.close_stream()
        self.__audio_player.open_stream()

    def set_callback(self,callback):
        self.callback = callback

    # Callbacks
    
    def __on_recording(self):
        if self.callback:
            self.callback()