'''
Basic script using default configuration settings to take a basic photo
'''
#https://raspberrytips.com/picamera2-raspberry-pi/ used to learn about camera python library
import time
from picamera2 import Picamera2, Preview

picam = Picamera2()

config = picam.create_preview_configuration()
picam.configure(config)

picam.start_preview(Preview.QTGL)

picam.start()
time.sleep(2)
picam.capture_file("first-image.jpg")
picam.close()