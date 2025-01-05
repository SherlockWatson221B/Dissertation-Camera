'''
Basic script for making a 10 second video using library picamera2
'''
#Tutorial followed https://raspberrytips.com/picamera2-raspberry-pi/ for using video functionality of picamera2 library
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

#Creates objects of picamera for setting up config
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

#Encoder used to produce video stream with bitrate number respresenting video quality
encoder = H264Encoder(10000000)

#Sleep determines the length of the video after the camera is started
picam2.start_recording(encoder, 'first_video.h264')
time.sleep(10)
picam2.stop_recording()