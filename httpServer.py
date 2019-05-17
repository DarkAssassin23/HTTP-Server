#!/usr/bin/python3
#Will Jones
#HTTP Server program
#I hereby declare upon my word of honor that I have neither given nor received unauthorized help on this work.
import socket
import datetime
import sys

# host (internal) IP address and port
HOST = "10.142.0.2"
PORT = 4040
# create our socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allow us to reuse an address for restarts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# set the socket host and port number up
sock.bind((HOST, PORT))

#keeps the socket open
while(True):
	#checks to see if there are internal errors and if there are any will
	#return 500
	try:
		#sets the defaluts for the code and output
		code = 200
		output = "HTTP/1.1 200 OK"
		# listen for any clients connecting
		sock.listen()

		# wait for a client to connect to us
		# accept a connection which has come through
		conn, addr = sock.accept()
		print("Connection from:", addr)

		# read some bytes from the client
		data = conn.recv(4096)

		# decode it into a string
		string = data.decode()
		#print(string)
		line = string.splitlines() #splits the string by lines
		line = line[0].split() # splits the first line into the components
		#checks if the length is less then three and returns 400
		if(len(line)<3):
			code = "<h1>400 Bad Request</h1>"
			output = "HTTP/1.1 400 Bad Request\n\n"
		#checks to see if it is any thing but GET and throws 405 exception
		elif(line[0]!="GET"):
			code = "<h1>405 Method Not Allowed</h1>"
			output = "HTTP/1.1 405 Method Not Allowed\n\n"
			#print("line length: "+str(len(line)))
			#print("line 1: "+line[0])
		#Checks if the final word is anything but HTTP/1.1 and throws
		#exception 505
		elif(line[len(line)-1]!="HTTP/1.1"):
			code = "<h1>505 HTTP Version Not Supported</h1>"
			output = "HTTP/1.1 505 HTTP Version Not Supported\n\n"
			#print("Last word: "+str(line[len(line)-1]))	
		#checks the file path and try to open that file
		else:	
			#if no path is given it opens the default index page
			if(line[1]=="/"):
				with open ('index.html', 'r') as myfile:
					page = myfile.read()
			else:
				#otherwise it tries to open the file given by the path
				try:
					with open (line[1][1:], 'r') as myfile:
						page = myfile.read()	
				#if the file doesn't exist with the path given 
				#it returns error 404 for it not being found
				except FileNotFoundError:
					code = "<h1>404 File Not Found</h1>"
					output = "HTTP/1.1 404 File Not Found"
				#if the file does exist but can't be opened it 
				#returns 403 for access is frobidden
				except PermissionError:
					code = "<h1>403 Forbidden</h1>"
					output = "HTTP/1.1 403 Forbidden"
	#if an internal error happens this exception is thrown to return 500
	except Exception:
		code = "<h1>500 Internal Server Error</h1>"
		output = "HTTP/1.1 500 Internal Server Error"
	#gets the current time and formats it
	now = datetime.datetime.now(datetime.timezone.utc)
	date = now.strftime("%a, %d %b %y %H:%M:%S GMT")
	#adds the date and other header information to the output
	output += "\nDate:"+date+" \nServer: CPSC 414 (Ubuntu)\n"
	output += "Content-Type: text/html; charset=UTF-8\nContent-Length: "
	#if no errors were found it get the file size and the file requested
	#and appends them to the output
	if(code==200):
		output += str(sys.getsizeof(page))+"\n\n\n"+page+"\n"
	#if an error was found it returns the size of the text for the error
	#as well as the error code and what it means
	else:
	 	output += str(sys.getsizeof(code))+"\n\n\n"+str(code)+"\n"
	# now encode the data for sending back
	data = output.encode()

	# send it back
	conn.sendall(data)

# and done
conn.close()

# done with listening on our socket to
sock.close()
