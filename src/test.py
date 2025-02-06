import hid
import time

# Find and connect to the Wiimote
wiimote = None
for device in hid.enumerate():
    if "nintendo" in device["product_string"].lower():
        wiimote = hid.Device(device["vendor_id"], device["product_id"])
        break

if not wiimote:
    print("No Wiimote found.")
    exit()


l1 = 0x10
l2 = 0x20
l3 = 0x40
l4 = 0x80

led = bytes([0x11, l1|l2|l3|l4, 0x00, 0x00])
wiimote.write(led)

time.sleep(.1)  # Wait for the response

led = bytes([0x11, 0x00, 0x00, 0x00])
wiimote.write(led)

for i in range(1, 101):
    hex_value = i  # `i` is already an int, no need to convert
    print(f"0x{hex_value:02X}")  # Format for display but keep it an int
    wiimote.write(bytes([0x15, 0x00]))  # Send as a byte
    data = wiimote.read(32)
    print(data)
    time.sleep(0.5)

exit()

try:
    while True:
        wiimote.write(bytes([0x00, 0x00]))
        data = wiimote.read(32)
        print(data)
except KeyboardInterrupt:
    print("Exiting...")
    wiimote.close()