FTPRetriever is based off of a program running on a few computers at an old job. 
The program would watch a folder for ".go" files and, if such a file were present,
would then check for a ".zip" or other file type with the same prefix. If that file
were found, the go file would be deleted and the other file would be transferred to a
predetermined FTP path. This sounded incredibly simple to do with Python and I was 
looking for some IT-related programs to practice, so I threw this together as a proof
of concept. I'll probably update it with argparse later so that file location, file 
type, FTP server and login/pw, and FTP path can be specified by user. Also, error detection.
