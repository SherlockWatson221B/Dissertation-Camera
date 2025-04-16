'''
This python file is going to be used to snip the mp4 video file into 30 second chunks every 15 minutes
'''
# Website provided the basic ffmpeg command to segment the videohttps://stackoverflow.com/questions/18444194/cutting-multimedia-files-based-on-start-and-end-time-using-ffmpeg 
# Website used for getting time out of the video file name https://docs.vultr.com/python/examples/extract-extension-from-the-file-name
# Websites use for converting string into a datetime object and extract from filename https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime https://docs.vultr.com/python/examples/extract-extension-from-the-file-name


import os
import subprocess
import time
from datetime import datetime, timedelta

class ffmpeg_segment ():
    '''
    Class designed for implementing the ffmpeg command to segmet video every 15 minutes for 30 seconds
    '''
    def __init__(self):
        # Directory where the mp4 video file is located
        self.target_directory = '/Users/Jasmine/Documents/Uni/Year3/Dissertation/'
        # Global variable for the video file which will passed in when calling method
        self.target_file = None
        # self.target_timestamps = ["00:00:00", "00:15:00", "00:30:00", "00:45:00", "01:00:00", "01:15:00", "01:30:00", "01:45:00", "02:00:00", "02:15:00", "02:30:00", "02:45:00", "03:00:00", "03:15:00", "03:30:00", "03:45:00"]
        self.target_timestamps = ["00:00:00", "00:15:00"]
    def segment_video(self, target_file):
        '''
        Method for segmenting the video into 30 second chunks using array with prediefined timestamps to run ffmpeg command
        This is designed to segment the video every 15 minutes into 30 second chunks
        '''
        # Joins the target directory with the targeet file name to create the full path
        target_full_file_path = os.path.join(self.target_directory, target_file)
        self.target_file = target_file
        # Used to extract the filename from the full filename with extenstion
        root, ext = os.path.splitext(target_file)
        # Converts the string filename into a datetime object to be used for new filename
        current_timestamp = datetime.strptime(root, '%Y-%m-%d_%H-%M-%S')
        print(current_timestamp)


        # Makes sure that the file exists in the directory
        if os.path.isfile(target_full_file_path):
            # For loop that iterates through the target timestamp array
            for time in self.target_timestamps:
                # Converting the timestamp into time that can be added to start time for file name
                h, m, s = map(int, time.split(':'))
                time = timedelta(hours=h, minutes=m, seconds=s)
                # Add time to the original timestamp to create new file name
                new_timestamp = current_timestamp + time
                # Converts the new timestamp into a string to be used for filename of new mp4 video
                new_timestamp_string = new_timestamp.strftime('%Y-%m-%d_%H-%M-%S')          
                print("\n\n\n\n\n\n")
                print(time)
                print(new_timestamp)


                # ffmpeg command to create a new mp4 file at a specfied time from a target mp4 file
                ffmpeg_command = [
                    'ffmpeg',
                    '-ss', f'{time}',
                    '-i', f'{target_full_file_path}', 
                    '-t', '30', 
                    '-c', 'copy', 
                    f'{new_timestamp_string}.mp4'
                ]
                #try except block used to catch any potential errors
                try:
                    subprocess.run(ffmpeg_command, check=True)
                    print("Successfully segmented part of the mp4 video")
                except Exception as e:
                    print(f"Error {e} occured when taking snippet of mp4 video")
        else:
            print("File was not found")

video_segmenter = ffmpeg_segment()
video_segmenter.segment_video('2025-04-16_11-05-00.mp4')
