import requests

# OpenRGB REST API URL
OPENRGB_URL = "http://127.0.0.1:6742"  # Default port


# Get a list of all devices
print("Getting list of devices...")
response = requests.get(f"{OPENRGB_URL}/devices", timeout=3)
devices = response.json()
print("Devices:")

# Print the names of all devices
for device in devices:
    print(device['name'])

