from openrgb import OpenRGB
import mido
import threading
import subprocess
import time
import json


client = OpenRGB('localhost', 6742) # open connection on port 6742 (OpenRGB default port)
devices = client.devices()

# get only the keyboard device
keyboard = next(devices) # change depending on where the keyboard is in the list
print('Connected to {}!\n'.format(keyboard.name))
all_led_ids = [i for i in range(len(keyboard.leds))]

def load_config():
    with open('config.json') as f:
        config = json.load(f)
    return config

# load config data
config = load_config()
midi_port_name = config['midi_port_name']
colors = config['colors']
note_mappings = config['note_mappings']

# determine which leds are in the numpad and keyboard area
numpad_led_ids = [note_data['led_id'] for note, note_data in note_mappings.items() if note_data['key'].startswith('num')]
keyboard_led_ids = [note_data['led_id'] for note, note_data in note_mappings.items() if not (note_data['key'].startswith('num'))]

# Mapping MIDI note numbers to note names
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# create a map with led_id as the key
led_colors = {}
for note, note_data in note_mappings.items():
    led_colors[note_data['led_id']] = colors['black']


def set_keyboard_color(new_color):
    color_collection = []
    for led_id in all_led_ids:
        if led_id in keyboard_led_ids:
            color_collection.append(new_color)
            led_colors[led_id] = new_color
        elif led_id in numpad_led_ids:
            prev_color = led_colors[led_id]
            color_collection.append(prev_color)
        else:
            color_collection.append((0, 0, 0))

    client.update_leds(color_collection)


def set_numpad_color(new_color):
    color_collection = []
    for led_id in all_led_ids:
        if led_id in numpad_led_ids:
            color_collection.append(new_color)
            led_colors[led_id] = new_color
        elif led_id in keyboard_led_ids:
            prev_color = led_colors[led_id]
            color_collection.append(prev_color)
        else:
            color_collection.append((0, 0, 0))

    client.update_leds(color_collection)


def set_led_color(led_id, new_color):
    client.update_single_led(led_id, new_color)
    led_colors[led_id] = new_color




# --- MIDI FUNCTIONS ---
def note_number_to_name(note_number):
    note_name = NOTE_NAMES[note_number % 12]
    octave = (note_number // 12) - 1  # MIDI note 0 is C-1
    return f"{note_name}{octave}"

def list_midi_ports():
    # List available MIDI input ports
    print("Available MIDI input ports:")
    for port in mido.get_input_names():
        print(port)
    print()

def listen_to_midi(port_name):
    # Open the specified MIDI input port and listen for messages
    with mido.open_input(port_name) as port:
        print(f"Listening on {port_name}")
        for message in port:
            print_message(message)
            handle_midi_message(message)

def print_message(message):
    if message.type == 'note_on':
        note_name = note_number_to_name(message.note)
        print(f"Note On: {note_name} Velocity: {message.velocity}")
    elif message.type == 'note_off':
        note_name = note_number_to_name(message.note)
        print(f"Note Off: {note_name}")

def handle_midi_message(message):
    if message.type == 'note_on':
        note_name = note_number_to_name(message.note)
        note_data = note_mappings.get(note_name)
        if note_data is None:
            return
        
        led_id = note_data['led_id']
        if led_id in keyboard_led_ids:
            set_led_color(led_id, colors['blue'])
        elif led_id in numpad_led_ids:
            set_led_color(led_id, colors['yellow'])

    elif message.type == 'note_off':
        note_name = note_number_to_name(message.note)
        note_data = note_mappings.get(note_name)
        if note_data is None:
            return
        
        led_id = note_data['led_id']
        set_led_color(led_id, colors['black'])





# --- MAIN ---
if __name__ == '__main__':
    set_keyboard_color(colors['black'])
    set_numpad_color(colors['black'])

    list_midi_ports()

    # listen_to_midi(midi_port_name)
    
    # Create a new thread that will run the handle_midi_messages function
    midi_thread = threading.Thread(target=listen_to_midi, args=(midi_port_name,))

    # Start the new thread
    midi_thread.start()

    # Wait for the thread to finish
    midi_thread.join()

    # reset the keyboard color
    set_keyboard_color(colors['black'])
    set_numpad_color(colors['black'])