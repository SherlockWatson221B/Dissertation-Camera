'''
This is initial code to test whether a file can be successfully uploaded to the webserver using SFTP. Credentials need to be
removed into an environment variable and not uploaded to github using gitignore.
'''
# Website used to help create script to connect to webserver using SFTP and send files https://docs.couchdrop.io/walkthroughs/using-sftp-clients/using-python-with-sftp
import paramiko
import os
# # Defining the filepath for remote and local file
# upload_file = '/Users/Jasmine/Documents/Uni/Year3/Dissertation/Dissertation/code/test/test.txt'
# target_file = '/httpdocs/BeeCafe/test.txt'

# # Defining the credientals for the webserver
# hostname = ''
# port = 22
# username = ''
# # REMEMBER TO SAVE PASSWORD IN ENVIRONMENT VARIABLE AND NOT UPLOAD TO GITHUB!!!!!!!!
# password = ''

# # Used to create a SSH client to create the secure tunnel for ftp
# ssh_client = paramiko.SSHClient()
# ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# # Connects to the webserver using SFTP with the credientals above
# ssh_client.connect(hostname, port, username, password)

# # Creates a new SFTP session
# sftp = ssh_client.open_sftp()

# # Command to upload a file to the webserver
# sftp.put(upload_file, target_file)

# # Class for uploading mp4 video chunks to the webserver to be displayed on the website
# class SFTPFileUpload:
#     def __init__(self):
#         # Defining the filepath for remote and local file
#         self.upload_file = '/Users/Jasmine/Documents/Uni/Year3/Dissertation/Dissertation/code/test/test2.txt'
#         self.target_file = '/httpdocs/BeeCafe/video/test2.txt'
#         # Defining the credientals for the webserver
#         hostname = ''
#         self.port = 22 # This is the default port for SFTP
#         self.username = ''
#         self.password = ''
#         self.ssh_client = paramiko.SSHClient()
#         self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
#     # Method for creating a new SFTP session
#     # Method for uploading a file to the webserver
#     def upload_file(self):
#         # Used to connect to the ssh client using the credientals
#         try:
#             self.ssh_client.connect(self.hostname, self.port, self.username, self.password)
#             # Opens a new SFTP session
#             self.sftp = self.ssh_client.open_sftp()
#         except Exception as e:
#             print(f"Error connecting to the webserver: {e}")
#         try:
#             self.sftp.put(self.upload_file, self.target_file)
#         except Exception as e:
#             print(f"Error uploading {self.upload_file} to {self.target_file} on the webserver: {e}")
#         try:
#             self.sftp.close()
#             self.ssh_client.close()
#         except Exception as e:
#             print(f"Error closing the SFTP session: {e}")

#     # Method for closing the SFTP session
#     def close(self):
#         try:
#             self.sftp.close()
#             self.ssh_client.close()
#         except Exception as e:
#             print(f"Error closing the SFTP session: {e}") 

class SFTPFileUpload:
    '''
    Class for uploading mp4 video chunks to the webserver to be displayed on the website
    '''
    def __init__(self):
        # Defining the filepath for remote and local file
        self.local_file_path = '/Users/Jasmine/Documents/Uni/Year3/Dissertation/Dissertation/code/test/video/'
        self.target_file_path = '/httpdocs/BeeCafe/video/'
        # Defining the credientals for the webserver
        self.hostname = ''
        self.port = 22 # This is the default port for SFTP
        self.username = ''
        self.password = ''
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    def get_files(self):
        '''
        Method for finding all of the mp4 files in the target directory and saves it to a list
        '''
        # List to store all mp4 files paths to be uploaded
        mp4_files = []
        # for loop that iterates through the target directory and saves the file paths to the list
        for root, directories, files in os.walk(self.local_file_path):
            for file in files:
                # Checks the file is an mp4 file before appending just incase a random files is in the directory
                if file.lower().endswith('.mp4'):
                    # Appends the file name of the mp4 to the list
                    mp4_files.append(file)
        # Returns the list of mp4 files to be used for uploading
        return mp4_files

    
    def connect(self):
        '''
        Method for creating a new SFTP session'''
        # Used to connect to the ssh client using the credientals
        try:
            self.ssh_client.connect(self.hostname, self.port, self.username, self.password)
            # Opens a new SFTP session
            self.sftp = self.ssh_client.open_sftp()
            print("Successfully connected to the webserver")
        except Exception as e:
            print(f"Error connecting to the webserver: {e}")

    def upload_file(self, filename):
        '''
        Method for uploading a file to the webserver
        '''
        # Joins the local target directory and remote target directory with the filename to be uploaded to allow multiple files
        local_full_file_path = os.path.join(self.local_file_path, filename)
        target_full_file_path = os.path.join(self.target_file_path, filename)
        try:
            self.sftp.put(local_full_file_path, target_full_file_path)
            print(f"File {local_full_file_path} uploaded to {target_full_file_path} successfully on the webserver")
        except Exception as e:
            print(f"Error uploading {local_full_file_path} to {target_full_file_path} on the webserver: {e}")

    def close(self):
        '''
        Method for closing the SFTP session
        '''
        try:
            self.sftp.close()
            self.ssh_client.close()
            print("SFTP session closed successfully")
        except Exception as e:
            print(f"Error closing the SFTP session: {e}")  

# Commands for testing the new class
uploader = SFTPFileUpload()
list_of_mp4_files = uploader.get_files()
uploader.connect()
for file in list_of_mp4_files:
    uploader.upload_file(file)
uploader.close()
