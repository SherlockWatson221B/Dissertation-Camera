'''
Test script for watchdog library to see if can work for monitoring a folder
to then trigger a ffmpeg method to take an mp4 video and segment it into 30 second videos.
'''
# Documentation and websites used to help create this python program
# Documentation for watchdog https://python-watchdog.readthedocs.io/en/stable/
# Documentation for logging https://docs.python.org/3/library/logging.html
# Documentation for ffmpeg https://ffmpeg.org/ffmpeg.html#Video-Options
# Documentation for running and using subprocesses to run ffmpeg command https://docs.python.org/3/library/subprocess.html
# Website used to test basic functionality of watchdog https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/
# Another websie https://www.pythonsnacks.com/p/python-watchdog-file-directory-updates also used to help create script and modify it to save logs to files which will be useful to remove the need to exec into the container to monitor 
# what is happening and keep a record of what is happening to files and when ffmppeg was used
# Website that was used to help with segmenting the mp4 video into sections https://community.gumlet.com/t/how-to-split-a-video-into-chunks-based-on-duration-using-ffmpeg/387
# Website used to find most effective way of running ffmpeg command in python https://www.gumlet.com/learn/ffmpeg-python/ subprocess was identified as best due to giving you full control
# Website used to help create script to connect to webserver using SFTP and send files https://docs.couchdrop.io/walkthroughs/using-sftp-clients/using-python-with-sftp


import os
import sys
import paramiko
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

# Class for uploading mp4 video chunks to the webserver to be displayed on the website
class SFTPFileUpload:
    def __init__(self):
        # Defining the filepath for remote and local file
        self.upload_file = '/Users/Jasmine/Documents/Uni/Year3/Dissertation/Dissertation/code/test/test2.txt'
        self.target_file = '/httpdocs/BeeCafe/test2.txt'
        # Defining the credientals for the webserver
        self.hostname = os.getenv("hostname")
        self.port = 22 # This is the default port for SFTP
        self.username = os.getenv("username")
        self.password = os.getenv("password")
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Method for creating a new SFTP session
    def connect(self):
        # Used to connect to the ssh client using the credientals
        try:
            self.ssh_client.connect(self.hostname, self.port, self.username, self.password)
            # Opens a new SFTP session
            self.sftp = self.ssh_client.open_sftp()
        except Exception as e:
            print(f"Error connecting to the webserver: {e}")

    # Method for uploading a file to the webserver
    def upload_file(self):
        try:
            self.sftp.put(self.upload_file, self.target_file)
        except Exception as e:
            print(f"Error uploading {self.upload_file} to {self.target_file} on the webserver: {e}")

    # Method for closing the SFTP session
    def close(self):
        try:
            self.sftp.close()
            self.ssh_client.close()
        except Exception as e:
            print(f"Error closing the SFTP session: {e}")    

# There is different levels of logging including DEBUG, INFO, WARNING, ERROR, CRITICAL
# Logging format has been outline here for the data and time and the message
logging.basicConfig(filename="recordings/watchdog_log_file.log",
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Class created to handle the different events that watchdog can monitor
# on_created on_deleted on_modified on_moved
# on_created will be used to run the ffmpeg command to segment the video
class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".mp4"):
            logging.info(f"New mp4 file discovered: {event.src_path}")
            # Here will be the ffmpeg command to segment the file into 30 second chunks
            # Code for uploading the files to the webserver when the video has been sugmented
            # Code for deleting the original mp4 file from directory on host
            # Code for deleting the 30 second video files from directory on host
        else:
            logging.info(f"File created: {event.src_path}")
    
    def on_deleted(self, event):
        logging.info(f"File deleted: {event.src_path}")
    
    def on_modified(self, event):
        # Used to stop the log file changes also being written to the log file increases readability of the log file
        if event.src_path.endswith(".log"):
            return
        logging.info(f"File modified: {event.src_path}")
    
    def on_moved(self, event):
        logging.info(f"File moved: {event.src_path} to {event.dest_path}")

if __name__ == "__main__":
    # Location of the directory that is being monitored
    # Recursive has been set to true meaning all directories within will also be watched
    path = "./recordings/input/"
    
    # Creates a new object for event handler which is defined above used to determine what to do on certain events
    event_handler = MyEventHandler()
    # Creating a new object for observer which is used to monitor the directory
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    # Try and except used to keep the observer running until the keyboard interrupt happens in this 
    # case it will run until the container is taken down as keybaord interrupts won't be needed
    try:
        # Used to start the observer allowing the directory to be monitored
        observer.start()
        logging.info("Watchdog observer has been started")
        while True:
            time.sleep(1)
    # If you control-c it will stop the observer and exit the python program
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Watchdog observer is in the process of being stopped")
    observer.join()
    logging.info("Watchdog observer has been stopped")