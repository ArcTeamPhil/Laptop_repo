import socket   #for sockets
import sys  #for exit
 
import yaml

try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
print 'Socket Created'
 
host = 'localhost'
port = 5000 
 
print 'Connected with ' + host + ':' + str(port)

'''
try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    ibam --totalbatterysys.exit()
     
print 'Ip address of ' + host + ' is ' + remote_ip
''' 
#Connect to remote server
s.connect((host , port))
 
##print 'Socket Connected to ' + host + ' on ip ' + remote_ip
 
#Send some data to remote server
message = "GET / HTTP/1.1\r\n\r\n"
 
try :
    #Set the whole string
    s.sendall(message)
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()
 
print 'Message send successfully'
