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
        array = np.zeros(9840)

        # init image array
        img = np.zeros( (60, 80), dtype = np.uint8)

        ## init data collection from socket 4920 + 82
        img_array = np.zeros( (4940,1), dtype=np.uint8)

        save_index = 0

        while True:
            print "\n"
            image_str = conn.recv(9840)


            #img_list = image_byte.split("\n")

            # CV2
            nparr = np.fromstring(image_str, np.uint16)

            ## each pixel is seperated by 30s, find all of them
            try:
                targets = [30, 31]
                thirty = np.where(nparr >=30 )[0]
                print "thirty", len(thirty)
                print nparr[0:10]
                ## whenever there is a disruption in the one off sequence, assume new row
                ## accomplish this by simpe subtraction 
                thirty_repeat = thirty[1::] - thirty[0:-1]
                ## a difference of more than 2 confirms this
                not_thirty_repeat =  np.where(thirty_repeat != 2)[0]
                not_thirty_diff = not_thirty_repeat[1::] - not_thirty_repeat[0:-1]

            except:
                #print "no thirties"
                print "data array: ", nparr[0:10]
                continue

            ## the first one begins the sequence of 164 len arrays
            ## as it is every other
            img_array = np.array( (nparr), dtype=np.uint8)
            #print "new ints: ", img_ints[0:5]

            ## first stream garbage
            if save_index < 3:
                save_index += 1
                continue
            else:
                pass
            print "starting img reassembly"
            img_start = not_thirty_repeat[0]*2 + 4

            if thirty[0] > 1:
                img_start += thirty[0]-1
            else:
                pass

            
            for i in range(len(not_thirty_repeat)-1):

                try:
                   
                    if not_thirty_diff[i] >= 80 and not_thirty_diff[i] < 82:
                        if i > 0:
                            guess = img_start + 164
                        else:
                            guess = img_start

                    elif not_thirty_diff[i] == 1:
                        continue
                    else:
                        guess = img_start + (not_thirty_diff[i]+2 ) * 2
                        print "################################# short: ", not_thirty_diff[i]


                    print "guess   : ", img_array[ guess-5: guess +5 ], img_array[guess]  ## expt 26*2  56
                    data_half = img_array[guess::2]
                    img_row = data_half[1:81]
                    img_row = np.array( (img_row), dtype=np.uint8)
                    row_index = img_array[guess]

                    if row_index > 60:
                            pass
                    else:
                        img[row_index,:] = img_row

                        img_start = guess

                    print "row updated"
                   
                except:
                    print "######################## pass, ", i
                    pass
            

            
            cv2.imshow('window_1', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            name = self.save_name + str(save_index) + '.png'
            if save_index >50 and save_index < 70:

                cv2.imwrite(name, img)
                print len(nparr)

                file_name = self.save_name + str(save_index) +'.txt'
                f_handle = file(file_name, 'a')
                np.savetxt(f_handle, np.transpose( nparr), \
                newline='\n', delimiter=',')
                f_handle.close()


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
