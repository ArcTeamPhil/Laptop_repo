#!/usr/bin/env python

import serial

# ser = serial.Serial('/dev/ttyACM1', 57600, bytesize=8, parity=serial.PARITY_NONE, timeout=0)

# print "connected to: " + ser.portstr
# count=0
# while True:
#      s = ser.read(8)
#      # for line in ser.readlines():   
#      #      print "line(" + str(count) + ")=" + line
#      #      count=count+1
#      count+= 1
#      print(s, count)

# ser.close()   

bytes()


# resultt =[]
# s = serial.Serial(port='/dev/ttyACM0', baudrate=57600, stopbits=1, timeout=3)
# instruct = bytes(('c', 'ascii'))
# s.write(instruct)
# data = s.read(1)
# if data:
#      print("yes")
# print("data: ", data)
# s.close()


ser = serial.Serial(port='/dev/ttyACM1', baudrate=57600, parity=serial.PARITY_NONE, stopbits=1, bytesize=serial.EIGHTBITS, timeout=2)
waiting = True
while waiting:
     # data = ser.readline()
     data = ser.read()
     print("data 1", data)
     # if 23591 == float(data):
     #      waiting = False

     # data = ser.readline()
     print("data", data)
ser.close()
