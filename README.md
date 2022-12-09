# Py Command Recorder GUI

## Description

Basic desktop app based in Python to record small audios to create a dataset for command recognition in machine learning.

The project is made using MVC ( Model View Controller ) architecture and the same idea as react to organize the sub-classed widgets as components.

- Standard library modules used:
 - Pyaudio - cross-platform audio input-output library, to easily reproduce and record audios.

 - Tkinter - Python native library to easily create GUI.

 - Matplotlib - A popular python library to plot data. Which I used to show the user the waveform of each recorded audio.

 - Numpy - Is a fundamental package for scientific computing in Python. But for this project, is used mainly for the special file format called NPZ, which is meant to behave as a compressed form of numpy array data, that also allows to separate each array by keyword same as a dictionary in Python. Taking advantage of this feature, I could store several audios for each command distiguished by a unique ID, which at the same time, allows to speficiy the data type of the array which reduces the space compared to store data in JSON.

- Project was made entirely in Python and tested in Windows 10.

## Setup

- Clone the repository in your local machine.
- Execute the `app.pyw` file to run the program.
- Click on open directory and select the folder where you want to read or create the audio commands.

## What I learned from this project

- I learned to appreciate the benefits from using MVC, which may seem difficult to understand at first, but as soon as the project increase in size and features, it makes it way easier to organize the whole code.

- Thanks to PyAudio, I better understand how audio I/O works, which kind of data audio requires, and how to reduce the amount of data needed specially for speech recognition, which allows to use the space more efficiently.

- Using same idea as React about create components, it makes easier to organize the inner features of each new component, keeping all the logic inside the component class rather than being present in the **View**.
And since the **Controller** should manage how the View behaves, each component includes a way to control their behaviour just managing what value is returned from their events callback.

- By using the NPZ format from Numpy


## Future Work
<!-- - ~~Done Task~~ ✅ -->
- Enhance user experience by showing toast or snackbar feedback while a command audios or a single audio is loading. 

- Allow confirm dialog to be cancelled or confirmed by keyboard to make it more ergonomic.

## Screencaps

### Command audio ( Youtube ) selected
![pythonw_Aw4xDoj5C3](https://user-images.githubusercontent.com/36393143/206805630-b3b1cb57-5390-4451-9170-ff31622e925f.png)

### Adding new command
![pythonw_fgslequPHt](https://user-images.githubusercontent.com/36393143/206805694-0b6079e4-7ad6-4c29-95ef-85817bf7e774.png)

### Confirm delete commands
![pythonw_MB1BhJb9mD](https://user-images.githubusercontent.com/36393143/206805604-d1817e1f-8abb-493d-965a-882aa6e40af1.png)

## Bugs to fix
<!-- - ~~Done Task~~ ✅ -->
- Freeze layout when confirmation dialog is open to prevent malfunction.
- Keep group buttons pressed when focus is loosed.
- Group frame scroll by mouse wheel is not working.
- Add New command must be cancelled on key press escape.
