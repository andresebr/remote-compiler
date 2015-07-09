#!/usr/bin/python
#Author: Andres E. Barreto

from socket import *

#Function definitions----------------------------------------------

def writeFile(filename, path, filecontent):
	f = open(path + filename, "w")
	f.write(filecontent)
	f.close()
	return

#------------------------------------------------------------------
#Type the serverName(String) and serverPort (int) where server.py is running

serverName = '<serverName>'
serverPort =  80


choice = "0"
while choice:
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName, serverPort))
	print """Menu
1) Compile a file in the server
2) Upload a file to the server
3) Download a file from the server"""
	choice = raw_input("Selection: ")
#----------------------------------------------------------------
	if "1" in choice:

		clientSocket.send(choice) #s1
		showlist = raw_input("Do you want to see a list of files stored in the server (y/n): ")
		clientSocket.send(showlist) #s2

		if "y" in showlist:
	
			filelist = clientSocket.recv(2048) #r1
			splittedfile = filelist.split(",")
			for i in range(0, len(splittedfile)):
				print splittedfile[i]

			filename = raw_input("Which file do yo want to compile? (filename.c): ")
			clientSocket.send(filename) #s3
			compileoutput = clientSocket.recv(2048) #r2
			print "OUTPUT:\n" + compileoutput
			saveoutput = raw_input("Do you want to save the results in a text file? (y/n): ")

			if "y" in saveoutput:

				savepath = raw_input("Where do you want to save the file? (/path/): ")
				outputfilename = filename + "-output.txt"
				writeFile(outputfilename, savepath, compileoutput)
				print outputfilename + " saved in " + savepath

		if "n" in showlist:

			filename = raw_input("Which file do yo want to compile? (filename.c): ")
			clientSocket.send(filename) #s3
			compileoutput = clientSocket.recv(2048) #r2
			print "OUTPUT:\n" + compileoutput
			saveoutput = raw_input("Do you want to save the results in a text file? (y/n): ")

			if "y" in saveoutput:

				savepath = raw_input("Where do you want to save the file? (/path/): ")
				outputfilename = filename + "-output.txt"
				writeFile(outputfilename, savepath, compileoutput)
				print outputfilename + " saved in " + savepath
			
		clientSocket.close()
#----------------------------------------------------------------
	elif "2" in choice:

		clientSocket.send(choice) #s1
		filepath = raw_input("Drag the file or write the location and name of the file you wish to upload (/path/fiename.c): ")
		filepath = filepath.replace("'","")
		filepath = filepath.replace(" ","")
		f = open(filepath,"r")
		filecontent = f.read()
		splittedpath = filepath.split("/")
		filename = splittedpath[len(splittedpath)-1]
		clientSocket.send(filename) #s2
		response = clientSocket.recv(2048) #r2
		print response
		clientSocket.send(filecontent) #s3
		response = clientSocket.recv(2048) #r3
		print response

		clientSocket.close()
#-----------------------------------------------------------------------
	elif "3" in choice:

		clientSocket.send(choice) #s1
		showlist = raw_input("Do you want to see a list of files stored in the server (y/n): ")
		clientSocket.send(showlist) #s2

		if "y" in showlist:

			
			filelist = clientSocket.recv(2048) #r1
			splittedfile = filelist.split(",")
			for i in range(0, len(splittedfile)):
				print splittedfile[i]
			filename = raw_input("Which file do yo want to download? (filename.c): ")
			clientSocket.send(filename) #s3
			filecontent = clientSocket.recv(2048) #r2
			downloadpath = raw_input("Where do you want to save the file? (/path/): ")
			writeFile(filename, downloadpath, filecontent)
			print filename + " downloaded in " + downloadpath

		elif "n" in showlist:

			filename = raw_input("Which file do yo want to download? (filename.c): ")
			clientSocket.send(filename) #s3
			filecontent = clientSocket.recv(2048) #r2
			downloadpath = raw_input("Where do you want to save the file? (/path/): ")
			writeFile(filename, downloadpath, filecontent)
			print filename + " downloaded in " + downloadpath
		
		clientSocket.close()

