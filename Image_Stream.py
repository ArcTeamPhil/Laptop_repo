import socket
import sys
from thread import *
import numpy as np
import cv2
import Image
import io
import StringIO
import os
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


        # init image array
        img_array = np.zeros( (60, 80), dtype = np.uint8)
        buffer = np.zeros( (2),dtype=int)
        bin_buffer = ''

        save_index = 0
        index = 0
        skip_index = 0
        while True:

            #print "\n"
            image_str = conn.recv( 9840)
            #print "data_type: ", type(image_str)
            # CV2
            array_16 = np.fromstring( image_str, np.uint16)
            array_8 =  np.fromstring( image_str, np.uint8)
            
            #data_save = np.fromstring(image_str, np.uint16)
            ### SAVING ###
            name = self.save_name + str(save_index) + '.png'
            
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

                ## collect every twentieth image
                if skip_index%20 == 0:

                    #print "image: ", save_index
                    img_array = np.reshape(buffer, (60,82))
                    img_array = img_array[:, 2::]
                    img_array /= 2.0**8
                    img_array = np.array(img_array, dtype=np.uint8)

                    cv2.imshow('window_1', img_array)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    else:
                        pass

                    if save_index < 3000:
                        #cv2.imwrite(name, img_array)
                        print "saving: ", save_index, "from: ", skip_index
                        file_name = self.save_name + str(save_index) +'.txt'
                        f_handle = file(file_name, 'a')

                        f_handle.write(bin_buffer)
                        f_handle.close()
                    else:
                        pass

                    save_index += 1
                else:
                    pass

            index += 1




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


    name = raw_input("enter save number: ")
    test_day = '/trial_10_1_' + name + '/'
    home_dir = '/media/phil/Backup_Drive_01/'
    for i in range(1,3):

        path = home_dir + "Lepton_" + str(i) + '/binary' + test_day
        print path
        if os.path.isdir(path):
            print "directory exists"
            break
        else:

            os.mkdir(path)

    if ports == 11540:
        name = home_dir + 'Lepton_1/binary/' + test_day 
    else:
        name = home_dir + 'Lepton_2/binary/' + test_day 
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
