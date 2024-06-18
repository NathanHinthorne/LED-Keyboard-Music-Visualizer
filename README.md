# LED Keyboard Music Visualizer

This is a simple MIDI visualizer that uses an LED keyboard to display the notes being played. It is written in Python and uses the `mido` library to read MIDI files and the `OpenRGB` library to light up keyboard LEDs. The visualizer is designed to work with the Redragon keyboard, but it can be easily modified for other keyboards.

## Usage

To use the visualizer, you must first edit the `config.json` file to match the LEDs on your keyboard. To identify which LEDs map to which keys, run `OpenRGB.exe` which you can install [here](https://openrgb.org/). 

Next, ensure you have a MIDI device connected to your computer. Finally, start the visualizer by running the `main.py` file.

## Dependencies

This application requires OpenRGB to be installed and running. You can download OpenRGB from [here](https://openrgb.org/).

After installing OpenRGB, you need to host its server locally. You can do this by opening OpenRGB and going to `SDK Server > Start server`.
