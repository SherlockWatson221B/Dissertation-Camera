'''
Basic script using default configuration settings to take a 5 second video
'''
#https://raspberrytips.com/picamera2-raspberry-pi/ used to learn about camera python library
#docker-rasbian-picam2 github repo helpped make changes necessary for containerisation
#https://artwilton.medium.com/running-ffmpeg-commands-from-a-python-script-676eaf2b2739 refresher for running ffmpeg commands in python
#https://www.w3schools.com/python/python_classes.asp used to debug a small syntax error when creating class
#https://www.w3schools.com/python/python_file_remove.asp Deleting a file with os
#https://stackoverflow.com/questions/68862565/running-scheduled-task-in-python used for implementing a scheduler to allow the camera to be run at specified times during the day
import os
import time
from time import sleep
import schedule
import datetime
import subprocess
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

class FFmpegCommand:
    '''
    Class for running ffmpeg command to convert raw binary file to mp4 file
    '''
    def __init__(self, ffmpeg_file):
        #Taken as input so file name can be the same for output and can change depending on day and time of video
        self.ffmpeg_file = ffmpeg_file

    def convert_file_mp4(self):
        #ffmpeg command to convert the file type
        ffmpeg_command = [
            'ffmpeg',
            '-framerate', '30',
            '-i', f'{self.ffmpeg_file}.h264',
            '-c', 'copy',
            f'recordings/{self.ffmpeg_file}.mp4'
        ]
        #try except block used to catch any potential errors
        try:
            subprocess.run(ffmpeg_command, check=True)
            print("Successfully converted file into mp4 file type")
            #Cleanup removing binary file after conversion
            #Checking file exists before attempting to remove
            if os.path.exists(f"{self.ffmpeg_file}.h264"):
                os.remove(f"{self.ffmpeg_file}.h264")
            else:
                print("File doesn't exist so couldn't be deleted")
        except Exception as e:
            print(f"Error {e} occured when converting to mp4 video")

class CaptureVideo:
    '''
    Class for creating a new video object to record for a specified length of time (11 - 4 everyday)
    '''
    def StartVideoCapture(self):
        '''
        Method for running the video recording
        '''
        #Creates object of picamera for setting up config
        picam2 = Picamera2()
        #config = picam2.create_video_configuration(main={"size": (1920, 1080)})
        config = picam2.create_video_configuration()
        picam2.configure(config)

        #Encoder used to produce video stream with bitrate number respresenting video quality
        encoder = H264Encoder(20000000)

        #Video file name
        file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        #Sleep determines the length of the video after the camera is started
        picam2.start_recording(encoder, f'{file_name}.h264')

        #Records for four hours
        #time.sleep(18001)
        time.sleep(1801)
        picam2.stop_recording()
        picam2.close()

        #Convert into a readable mp4 format
        mp4_converter = FFmpegCommand(file_name)
        mp4_converter.convert_file_mp4()

class video_scheduler:
    '''
    Class that is responsible for creating a schedule to allow the video to record between the hours of 11 - 4 each day
    '''
    def schedule_video_recording_job(self):
        '''
        Method for creating a scheduler to allow a jon to be run at a specified time period
        '''
        #Every day at 11:00 the recording will start
        schedule.every().day.at('10:10').do(self.video_recording_job)

        #Checks to see if there is any schedule task that are waiting to run
        while True:
            schedule.run_pending()
            #How long it waits before checking again used to give the cpu a break
            sleep(1)
    def video_recording_job(self):
        '''
        Method that allows the new object to be created to start the video recording
        '''
        Video_capture = CaptureVideo()
        Video_capture.StartVideoCapture()
#Creating a new scheduler object
#Running the method that is responsible for creating the new scheduler to run the method that creates the new video object
scheduler = video_scheduler()
scheduler.schedule_video_recording_job()