#!/usr/bin/python
#Author: Andres E. Barreto

import os
import glob
import subprocess
from socket import *

#Function definitions----------------------------------------------

def writeFile(filename, path, filecontent):
	f = open(path + filename, "w")
	f.write(filecontent)
	f.close()
	return

def openFile(filename, path):
	f = open(path + filename,"r")
	filecontent = f.read()
	return filecontent

def compileSource(filename, path):
	splittedfilename = filename.split(".")
	extension = splittedfilename[len(splittedfilename)-1]
	name = splittedfilename[0]
	if extension == "py":
		output = subprocess.check_output("python " + path + filename, shell=True)
		return output
	elif extension == "c" or extension == "cpp":
		subprocess.call("gcc " + path + filename + " -o " + path + name, shell=True)
		output = subprocess.check_output(path + name, shell=True)
		return output
	elif extension == "java":
		subprocess.call("javac " + path + filename, shell=True)
		output = subprocess.check_output("CLASSPATH=" + path +  " java " + name, shell=True)
		return output
	else:
		return "File format not supported.\n"
		
#------------------------------------------------------------------

path = os.path.dirname(os.path.abspath(__file__)) + "/server_files/"
if not os.path.exists(path):
    os.makedirs(path)



serverPort = 12003
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print "The server is ready to receive"

while 1:
	connectionSocket, addr = serverSocket.accept()
	choice = connectionSocket.recv(2048) #r1
#----------------------------------------------------------------------
	if "1" in choice:

		print "Ready to compile"
		showlist = connectionSocket.recv(2048) #r2

		if "y" in showlist:

			print "Sending a list of files in " + path
			os.chdir(path)
			filelist = ""
			for files in glob.glob("*.*"):
				filelist = files + "," + filelist 	
			filelist = filelist[:-1]			
			connectionSocket.send(filelist)#s1
			filename = connectionSocket.recv(2048) #r3
			print "Compiling " + filename
			output = compileSource(filename, path)
			print "Sending " + filename + " results..."
			connectionSocket.send(output) #s2

		elif "n" in showlist:

			filename = connectionSocket.recv(2048) #r3
			print "Compiling " + filename
			output = compileSource(filename, path)
			print "Sending " + filename + " results..."
			connectionSocket.send(output) #s2
		
		print "Results of " + filename + " compilation sent"
		print "The server is ready to receive"

 		connectionSocket.close()
#----------------------------------------------------------------------
	if "2" in choice:

		print "Ready to receive a file"
		filename = connectionSocket.recv(2048) #r2
		connectionSocket.send("Uploading " + filename + " to the server") #s2
		filecontent = connectionSocket.recv(2048) #r3
		print filename + " received"
		writeFile(filename, path, filecontent)
		print filename + " saved in " + path
		connectionSocket.send(filename + " uploaded successfully to " + path + " in the server.") #s3
		print "The server is ready to receive"
		connectionSocket.close()
#-----------------------------------------------------------------------
	if "3" in choice:

		print "Ready to send a file"
		showlist = connectionSocket.recv(2048) #r2

		if "y" in showlist:

			print "Sending a list of files in " + path
			os.chdir(path)
			filelist = ""
			for files in glob.glob("*.*"):
				filelist = files + "," + filelist 	
			filelist = filelist[:-1]
			connectionSocket.send(filelist)#s1
			filename = connectionSocket.recv(2048) #r3
			print filename + " requested"
			filecontent = openFile(filename, path)
			print "Sending " + filename + " ..."
			connectionSocket.send(filecontent) #s2
			
		elif "n" in showlist:
			
			filename = connectionSocket.recv(2048) #r3
			print filename + " requested"
			filecontent = openFile(filename, path)
			print "Sending " + filename + " ..."
			connectionSocket.send(filecontent) #s2
		
		print "The server is ready to receive"	 
		connectionSocket.close()
	
