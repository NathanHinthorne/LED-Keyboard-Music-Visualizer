import mido


# OpenRGB REST API URL
OPENRGB_URL = "http://localhost:6742"  # Default port

# might need these layouts to locate adjacent keys (e.g. for ripple effects)
keyboard = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
]

# num pad should be yellow and do ripples starting from the center for PERCUSSION
numpad = [
    ['n7', 'n8', 'n9'],
    ['n4', 'n5', 'n6'],
    ['n1', 'n2', 'n3']
]


note_mappings = {

    # row 1
    'C6': {'key': '0', 'led_id': 31, 'color': (0, 0, 0)},
    'B5': {'key': '9', 'led_id': 30, 'color': (0, 0, 0)},
    'A#5': {'key': '8', 'led_id': 29, 'color': (0, 0, 0)},
    'A5': {'key': '7', 'led_id': 28, 'color': (0, 0, 0)},
    'G#5': {'key': '6', 'led_id': 27, 'color': (0, 0, 0)},
    'G5': {'key': '5', 'led_id': 26, 'color': (0, 0, 0)},
    'F#5': {'key': '4', 'led_id': 25, 'color': (0, 0, 0)},
    'F5': {'key': '3', 'led_id': 24, 'color': (0, 0, 0)},
    'E5': {'key': '2', 'led_id': 23, 'color': (0, 0, 0)},
    'D#5': {'key': '1', 'led_id': 22, 'color': (0, 0, 0)},

    # row 2
    'D5': {'key': 'p', 'led_id': 52, 'color': (0, 0, 0)},
    'C#5': {'key': 'o', 'led_id': 51, 'color': (0, 0, 0)},
    'C5': {'key': 'i', 'led_id': 50, 'color': (0, 0, 0)},
    'B4': {'key': 'u', 'led_id': 49, 'color': (0, 0, 0)},
    'A#4': {'key': 'y', 'led_id': 48, 'color': (0, 0, 0)},
    'A4': {'key': 't', 'led_id': 47, 'color': (0, 0, 0)},
    'G#4': {'key': 'r', 'led_id': 46, 'color': (0, 0, 0)},
    'G4': {'key': 'e', 'led_id': 45, 'color': (0, 0, 0)},
    'F#4': {'key': 'w', 'led_id': 44, 'color': (0, 0, 0)},
    'F4': {'key': 'q', 'led_id': 43, 'color': (0, 0, 0)},

    # row 3
    'D4': {'key': ';', 'led_id': 73, 'color': (0, 0, 0)},
    'C#4': {'key': 'l', 'led_id': 72, 'color': (0, 0, 0)},
    'C4': {'key': 'k', 'led_id': 71, 'color': (0, 0, 0)},
    'B3': {'key': 'j', 'led_id': 70, 'color': (0, 0, 0)},
    'A#3': {'key': 'h', 'led_id': 69, 'color': (0, 0, 0)},
    'A3': {'key': 'g', 'led_id': 68, 'color': (0, 0, 0)},
    'G#3': {'key': 'f', 'led_id': 67, 'color': (0, 0, 0)},
    'G3': {'key': 'd', 'led_id': 66, 'color': (0, 0, 0)},
    'F#3': {'key': 's', 'led_id': 65, 'color': (0, 0, 0)},
    'F3': {'key': 'a', 'led_id': 64, 'color': (0, 0, 0)},

    # row 4
    'D3': {'key': '/', 'led_id': 95, 'color': (0, 0, 0)},
    'C#3': {'key': '.', 'led_id': 94, 'color': (0, 0, 0)},
    'C3': {'key': ',', 'led_id': 93, 'color': (0, 0, 0)},
    'B2': {'key': 'm', 'led_id': 92, 'color': (0, 0, 0)},
    'A#2': {'key': 'n', 'led_id': 91, 'color': (0, 0, 0)},
    'A2': {'key': 'b', 'led_id': 90, 'color': (0, 0, 0)},
    'G#2': {'key': 'v', 'led_id': 89, 'color': (0, 0, 0)},
    'G2': {'key': 'c', 'led_id': 88, 'color': (0, 0, 0)},
    'F#2': {'key': 'x', 'led_id': 87, 'color': (0, 0, 0)},
    'F2': {'key': 'z', 'led_id': 86, 'color': (0, 0, 0)},

    # numpad
    
    # 'n7': 59,
    # 'n8': 60,
    # 'n9': 61,
    # 'n4': 80,
    # 'n5': 81,
    # 'n6': 82,
    # 'n1': 101,
    # 'n2': 102,
    # 'n3': 103
}

def assign_color_gradient(start_color, gradient_step):
    for index, note in enumerate(note_mappings):
        color = (
            start_color[0] + index * gradient_step[0],
            start_color[1] + index * gradient_step[1],
            start_color[2] + index * gradient_step[2]
        )
        note_mappings[note]['color'] = color

def update_leds():
    for note in note_mappings:
        led_id = note_mappings[note]['led_id']
        color = note_mappings[note]['color']
        set_key_color(0, led_id, color)

def set_key_color(device_id, led_id, color):
    data = {
        "id": device_id,
        "leds": [
            {
                "id": led_id,
                "color": {
                    "red": color[0],
                    "green": color[1],
                    "blue": color[2]
                }
            }
        ]
    }
    response = requests.post(f"{OPENRGB_URL}/device/update", json=data)
    if response.status_code != 200:
        print(f"Failed to set color: {response.text}")

# MIDI callback function
def midi_callback(message):
    if message.type == 'note_on':
        note = message.note
        led_id = note_mappings.get(note)['led_id']
        if led_id is not None:
            set_key_color(0, led_id, (255, 0, 0))  # Red color

# Open MIDI input port
# with mido.open_input('Your MIDI Device Name') as port:
#     for message in port:
#         midi_callback(message)



# Get a list of all devices
print("Getting list of devices...")
response = requests.get(f"{OPENRGB_URL}/devices", timeout=3)
devices = response.json()
print("Devices:")

# Print the names of all devices
for device in devices:
    print(device['name'])

