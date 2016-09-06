import socket
import sys
from thread import *
import numpy as np
import cv2
import Image
import io
import StringIO
from array import array

## create class for opening and running sockets


class sockets():

    def __init__(self, ports, name):

        self.FRAMESIZE = 9840
        self.ROWS = 60
        self.COLS = 80
        self.ROWSIZE = 164
        self.MIN_TEMP = 8100
        self.MAX_TEMP = 8400
        self.save_name = name

        self.index = 0
        self.dist = 0
        self.dumpFrame = False
        self.ports = ports
        self.host = ''

        self.sock = ''
        self.conn = ''
        self.addr = ''

        self.frame = bytearray([])

        cv2.namedWindow('window_1', cv2.WINDOW_NORMAL)

    def sock_open(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'

        

        try:
            self.sock.bind((self.host, self.ports))
            print 'Bind Successful'

        except socket.error , msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        self.sock.listen(10)
        print 'Socket now listening'



    def client_thread(self, conn):

        #Sending message to connected client
        #conn.send('Welcome to the server. Type something and hit enter\n')
        #send only takes string

        #infinite loop so that function do not terminate and thread do not end.
        array = np.zeros(1024)

        # init image array
        img = np.zeros( (60, 80), dtype = np.uint8)

        ## init data collection from socket 4920 + 82
        img_array = np.zeros( (4920,1), dtype=np.uint8)

        save_index = 0

        while True:

            image_str = conn.recv(1024)


            #img_list = image_byte.split("\n")

            # CV2
            nparr = np.fromstring(image_str, np.uint8)

            

            #f_handle = file("test_array_7.txt", 'a')
            #np.savetxt(f_handle, np.transpose( nparr), \
            #newline='\n', delimiter=',')
            #f_handle.close()

            #nparr = np.reshape(nparr, (32,32))
            #img_np = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_GRAYSCALE) ##COLOR) #  in OpenCV 3.

            ## seperate current data stream
            img_ints = nparr[1::2]

            ## begin appending to img array
            img_array = np.append( img_array, img_ints)

            max_index = 0

            img_array = np.array( (img_array), dtype=np.uint8)
            #print "new ints: ", img_ints[0:5]

            for k in range(59):
                try:

                    index = np.where(img_array == k)
                    index = index[0][0] + 2

                    index_end = np.where(img_array == k+1)
                    index_end = index_end[0][0]

                    #print "index length: ", index_end - index
                    fract_update = index_end - index
                    if fract_update > 80:
                        continue

                    img[k,:] = np.array( ( img_array[index:index+80]) )

                    #print "updated image", k
                    if index > max_index:
                        max_index = index + 82

                except:
                    pass

            img = np.array( (img), dtype =np.uint8)

            cv2.imshow('window_1', img)

            ## remove all content that came befor int end
            img_array = img_array[max_index::]

            #print "new img array length: ", len(img_array)

            name = self.save_name + str(save_index) + '.png'
            cv2.imwrite(name, img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            save_index += 1



        #came out of loop
        conn.close()







    def sock_stream(self):

        while True:

            #wait to accept a connection - blocking call

            self.conn, self.addr = self.sock.accept()

            #display client information
            print 'Connected with ' + self.addr[0] + ':' + str(self.addr[1])
            #now keep talking with the client
            #start new thread takes 1st argument as a function name to be run,
            #second is the tuple of arguments to the function.
            
            start_new_thread(self.client_thread ,( self.conn,))


        ## in case of failure, close connection
        self.conn.close()
        ## close socket always
        self.sock.close()


if __name__ == '__main__':

    ports = int ( raw_input("enter port: ") )

    name = raw_input("enter save name: ")

    if ports == 11540:
        name = '/media/phil/Backup_Drive_01/Lepton_1/' + name + '_'
    else:
        name = '/media/phil/Backup_Drive_01/Lepton_2/' + name + '_'
    try:

        exe = sockets(ports, name)
        exe.sock_open()

        x = True
        while (x== True):
            exe.sock_stream()

            ## end process
            if cv2.waitKey(1) & 0xFF == ord('q'):
                x = False
                break

    except KeyboardInterrupt:

        pass
    '''
    finally:
        conn = exe.conn
        conn.close()
    '''
