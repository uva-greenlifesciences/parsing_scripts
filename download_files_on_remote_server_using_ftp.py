from ftplib import FTP
import os
import glob
import gzip

directory_path_for_downloaded_files = "/Users/mgalland/GoogleDrive/UvA_POSTDOC_2014-2017/data/rfam/"

ftp = FTP("ftp.ebi.ac.uk") # use ftp protocol to connect to a distant ftp server
ftp.login() # anonymous login
#ftp.retrlines('LIST') # list all files in directory

ftp.cwd("/pub/databases/Rfam/CURRENT/fasta_files/")

filenames = ftp.nlst()[1:] # return a list of all files in the specified directory
print filenames[0:5]

print "Here is the number of files available to download: {0}".format(len(filenames))

# Iterate through all the filenames and retrieve them one by one:
for filename in filenames:
		local_filename = os.path.join(directory_path_for_downloaded_files,filename) # open a local file for writing in binary mode
		with open(local_filename,"wb") as fileout: # the "with" statement ensures that the file is closed at the end
			def callback(data):
				fileout.write(data)

			ftp.retrbinary("RETR %s" % filename, callback)
	
ftp.quit()

# Unzip the .gz files
for gunzip_file in glob.glob(directory_path_for_downloaded_files+"*.gz"):
	with gzip.open(gunzip_file,"rb") as filin:
		filin_content = filin.read()
		with open(gunzip_file[:-3],"wb") as fileout:
			fileout.write(filin_content)
