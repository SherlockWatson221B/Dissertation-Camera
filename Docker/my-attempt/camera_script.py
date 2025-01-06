'''
Basic script using default configuration settings to take a basic photo
'''
#https://raspberrytips.com/picamera2-raspberry-pi/ used to learn about camera python library
#docker-rasbian-picam2 github repo helpped make changes necessary for containerisation
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

#Creates object of picamera for setting up config
picam2 = Picamera2()
config = picam2.create_video_configuration()
picam2.configure(config)

#Encoder used to produce video stream with bitrate number respresenting video quality
encoder = H264Encoder(10000000)

#Sleep determines the length of the video after the camera is started
picam2.start_recording(encoder, 'first_video.h264')
time.sleep(5)
picam2.stop_recording()
picam2.close()