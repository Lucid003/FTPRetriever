"""
I will need timeout detection that will restart the process and not delete the file prematurely
I will also need other error detection, so don't forget
"""

import os
import ftplib
from time import perf_counter

print("Script started")
time_stamp = perf_counter()
while True:
    if perf_counter() - time_stamp >= 5: # if it's been 5 seconds since time_stamp
        print("Checking for files")
        time_stamp = perf_counter() # reset time_stamp
        path = 'C:/process_files/'
        path_contents = os.listdir(path)
        for file in path_contents:
            if file[-3:] == '.go': # if file ends in '.go'
                try:
                    upload_file = file[:-3] + ".zip" # If the go file exists, we're assuming a zip file does, as well
                    print("File found, connecting to FTP")
                    ftp = ftplib.FTP('demo.wftpserver.com') # Create FTP object
                    print("Logging into FTP")
                    ftp.login('demo', 'demo') # Login to FTP server
                    ftp.cwd('/upload/') # navigate to upload directory
                    print('Transfering file: {}'.format(os.path.join(path, upload_file)))
                    print("{}".format(os.path.join(path, file[:-3] + ".zip")))
                    ftp.storbinary('STOR ' + upload_file, open(os.path.join(path, upload_file), 'rb')) # send the file
                    print('Deleting file: {}'.format(os.path.join(path, file)))
                    print('Deleting file: {}'.format(os.path.join(path, upload_file)))
                    os.remove(os.path.join(path, file)) # delete the go file
                    os.remove(os.path.join(path, upload_file)) # delete the zip file
                except ftplib.all_errors as e:
                    print(e)


