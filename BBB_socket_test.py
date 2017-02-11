import numpy as np
import socket
import sys
import cv2
import os

HOST = ''
PORT = 11540# Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
s.listen(10)
print 'Socket now listening'
 
#now keep talking with the client

#wait to accept a connection - blocking call
conn, addr = s.accept()



cv2.namedWindow('window_1', cv2.WINDOW_NORMAL)
cv2.resizeWindow('window_1', 800, 800)

img_array = np.zeros( (60, 80), dtype = np.uint8)
buffer = np.zeros( (2),dtype=int)
bin_buffer = ''

save_index = 0
index = 0
skip_index = 0

print 'Connected with ' + addr[0] + ':' + str(addr[1])
while 1:
     
    image_str = conn.recv(9840)


    #array_16 = np.fromstring( image_str, np.uint16)

    #print array_16





    array_16 = np.fromstring( image_str, np.uint16)
    array_8 =  np.fromstring( image_str, np.uint8)

    #data_save = np.fromstring(image_str, np.uint16)

    buffer = np.append(buffer, array_16)
    bin_buffer += image_str

    if index == 0:
        buffer = buffer[2::]
    else:
        pass

    if len(buffer) > 4920:
        buffer = array_16
        bin_buffer = image_str

    elif len(buffer) == 4920:
        skip_index += 1


        #print "image: ", save_index
        img_array = np.reshape(buffer, (60,82))
        img_array = img_array[:, 2::]
        img_array /= 2.0**8
        img_array = np.array(img_array, dtype=np.uint8)

        img_array = cv2.applyColorMap(img_array, cv2.COLORMAP_JET)
        cv2.imshow('window_1', img_array)




        #cv2.imwrite(name, img_array)
        print "saving: ", save_index, "from: ", skip_index

        #os.chdir("../Lepton_1/trial_11_25_0")

        file_name =  str(save_index) +'.txt'


        f_handle = file(file_name, 'a')

        f_handle.write(bin_buffer)
        f_handle.close()



        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        else:
            pass

        save_index += 1

    index += 1
    ##conn.sendall(reply)
 
conn.close()
s.close()
