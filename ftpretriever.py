"""
I will need timeout detection that will restart the process and not delete the file prematurely
I will also need other error detection, so don't forget
"""

import argparse
import os
import ftplib
from time import perf_counter

def main():
    parser = argparse.ArgumentParser(
              'FTP Retriever',
              description="""Monitors a location for .go files. If .go file is present,
              will check for another file with the same prefix and a user-chosen extension
              and then upload that file to an FTP location before deleting the .go file
              and the FTP'd file. 
              """
              )
    parser.add_argument('-s', '--source',
                        help='Source folder path. Ex: -s C:\source',
                        required=True,
                        dest='path')
    parser.add_argument('-d', '--dest',
                        help='Destination path on FTP server. Ex: -d /upload/',
                        required=True,
                        dest='dest_path')
    parser.add_argument('-f', '--ftp',
                        help='FTP Server. Ex: -f demo.wftpserver.com',
                        required=True,
                        dest='server')
    parser.add_argument('-u', '--user',
                        help="""FTP Login Name. Ex: -u User01
                        This argument is not required, but
                        script will fail if FTP server requires
                        a user name and none is provided.""",
                        dest='user')
    parser.add_argument('-p', '--pass',
                        help="""FTP Login Password. Ex: -p Password99
                        This argument is not required, but
                        script will fail if FTP server requires
                        a user name and none is provided.""",
                        dest='password')
    parser.add_argument('-e', '--extension',
                        help="""Extension of files to be transferred. Ex: zip
                        Does not currently support multiple types.
                        Script will not work if user enters a period here.""",
                        required=True,
                        dest='extension',
                        )
                      
    
    args = parser.parse_args()

    print("Script started")
    time_stamp = perf_counter()
    while True:
        if perf_counter() - time_stamp >= 5: # if it's been 5 seconds since time_stamp
            print("Checking for files")
            time_stamp = perf_counter() # reset time_stamp
            path_contents = os.listdir(args.path)
            for file in path_contents:
                if file[-3:] == '.go': # if file ends in '.go'
                    try:
                        upload_file = file[:-3] + ".{}".format(args.extension) # If the go file exists, we're assuming a zip file does, as well
                        print("File found, connecting to FTP")
                        ftp = ftplib.FTP(args.server) # Create FTP object
                        print("Logging into FTP")
                        ftp.login(args.user, args.password) # Login to FTP server
                        ftp.cwd(args.dest_path) # navigate to upload directory
                        print('Transfering file: {}'.format(os.path.join(args.path, upload_file)))
                        print("{}".format(os.path.join(args.path, file[:-3] + ".zip")))
                        ftp.storbinary('STOR ' + upload_file, open(os.path.join(args.path, upload_file), 'rb')) # send the file
                        print('Deleting file: {}'.format(os.path.join(args.path, file)))
                        print('Deleting file: {}'.format(os.path.join(args.path, upload_file)))
                        os.remove(os.path.join(args.path, file)) # delete the go file
                        os.remove(os.path.join(args.path, upload_file)) # delete the zip file
                    except ftplib.all_errors as e:
                        print(e)

if __name__ == '__main__':
    main()
