import numpy as np
import cv2
import os
from scipy import misc
import time
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import exifread


class img_proc():

    def __init__(self, trials):

        self.var_dict_ = {}
        self.var_dict_["trials"] = trials
        self.var_dict_["data_path"] = '/media/phil/Backup_Drive_01'
        self.var_dict_["win_dim"] = [350, 500]
        self.var_dict_["win_name"] = [None]*len(trials)*2
        self.var_dict_["cam_folders"] = ['Lepton_1/imgs/', 'Lepton_2/imgs/']
        self.var_dict_["bin_folders"] = ['Lepton_1/binary', 'Lepton_2/binary']
        self.var_dict_["img_roi"] = [ [35,33], [39,34]]
        
        print self.var_dict_["win_name"]
        self.data_dict_ = {}
        self.data_dict_["buffer"] = np.zeros( (2),dtype=int)
        self.data_dict_["img_0"] = np.zeros( (60, 80), dtype = np.uint8)
        self.data_dict_["img_1"] = np.zeros( (60, 80), dtype = np.uint8)
        self.data_dict_["bin_img_0"] =  np.zeros( (60, 80), dtype = np.uint16)
        self.data_dict_["bin_img_1"] =  np.zeros( (60, 80), dtype = np.uint16)
        self.data_dict_["int_0"] = np.zeros( (850), dtype = np.uint16)
        self.data_dict_["int_1"] = np.zeros( (850), dtype = np.uint16)


        ## create windows for viewing images
        self.index = 0
        for i in range( len(self.var_dict_["win_name"]) ):
            self.var_dict_["win_name"][self.index] = 'window' + str(self.index)
            cv2.namedWindow( self.var_dict_["win_name"][self.index], cv2.WINDOW_NORMAL)
            self.index += 1
            
        self.index = 0
        self.radius = 5.0

        ## plot histogram for images
        plt.ion()

        self.fig, self.cxs = plt.subplots(1,2, facecolor='w', edgecolor='k' )

        for i in range(2):
          self.cxs[i] = plt.gca()

          self.cxs[i].set_ylim([0, 2**12])
          self.cxs[i].set_xlim([0,850])


          self.x = np.linspace(0,850, 850)
          self.y = np.zeros(850, dtype=np.uint16)
          tag = "int_" + str(i)
          self.cxs[i].plot( self.x, self.data_dict_[tag])


       
    def load_imgs(self, index):

        for cam in self.var_dict_["cam_folders"]:
            ## move to folders

            img_dir = os.path.abspath( os.path.join(self.var_dict_["data_path"], cam)) 

            
            for j in trials:

                img_path = os.path.join(img_dir, j)
                first_trial = os.listdir(img_path)[0]
                img_base = str(first_trial)
                base_len = img_base.rfind('_')
                img_base = img_base[0:base_len+1]


                file_len = len( os.listdir(img_path))


                img_name = img_base + str(index) + '.png'
                img_path = os.path.join(img_path, img_name)
                img = misc.imread(img_path, 0)

                f = open(img_path, 'rb')
                tags = exifread.process_file(f)
                f.close()
                #print tags
                tag = "img_" + str(self.index)
                self.data_dict_[tag] = img

                self.index += 1
        self.index = 0

    def load_bin(self, index):

        
        for cam in self.var_dict_["bin_folders"]:
            ## move to folders

            bin_dir = os.path.abspath( os.path.join(self.var_dict_["data_path"], cam)) 

            for j in trials:

                ## move to appropriate directory
                bin_path = os.path.join(bin_dir, j)
                ## grab first file in dir
                first_trial = os.listdir(bin_path)[0]
                ## convert to str
                bin_base = str(first_trial)
                ## grab all content before iteration numbering
                base_len = bin_base.rfind('_')
                bin_base = bin_base[0:base_len+1]

                ## grab the full file name of binary file
                bin_name = bin_base + str(index) + '.txt'
                ## join the name with the path
                bin_path = os.path.join(bin_path, bin_name)
                ## open the file and read it
                f = open(bin_path, 'r')

                image_str = f.read()

                f.close()
                ## set the tag mark for the dictionary
                tag = "bin_img_" + str(self.index + 1)

                ## convert binary to unsigned 16 bit
                array_16 = np.fromstring( image_str, np.uint16)

                ## create the buffer the inverse image will go into
                buffer = np.ones(len(array_16), dtype = np.uint16)*(2**16-1)

                ## subtract the two
                buffer -= array_16

                ## use top  three rows as normalization location
                '''
                hist_equ = np.median(buffer[0:3*80])
                #print hist_equ
                #hist_equ = 65535.0 /10.0
                buffer = buffer - hist_equ

                buff_neg = np.where(buffer < 0)[0]
                buffer[buff_neg] = 0
                #buffer /= hist_equ

                buffer = buffer / (2.0**16-hist_equ)*255
                buffer = np.array( buffer, dtype = np.uint8)
                #print max(buffer)
                '''
                buffer = buffer /2.0**8
                
                ## rearrange buffer to image size and pre-info
                self.data_dict_[tag] = np.reshape( buffer, (60,82) )
                ## remove pre-info
                self.data_dict_[tag] = self.data_dict_[tag][:, 2::]



                self.index += 1
        self.index = 0
        

    def proc_img(self,index):

        self.index = 0
        for cam in self.var_dict_["bin_folders"]:

            roi = self.var_dict_["img_roi"][self.index]
            mask = np.zeros( (60,80), dtype=np.uint8)

            ## draw green (0,255,0) circle over nostril
            cv2.circle(mask,(roi[1], roi[0]), int(self.radius), 255,-1)

            focus = np.where( mask == 255)[0]

            tag = "bin_img_" + str(self.index+1)

            intensity = np.sum( self.data_dict_[tag][focus] ) / np.pi / self.radius**2
            
            tag = "int_" + str(self.index)
            self.data_dict_[tag][index] = intensity


            tag = "bin_img_" + str(self.index+1)
            cv2.circle(self.data_dict_[tag], (roi[1], roi[0]), int(self.radius), 255, 1)

            self.index += 1


    def view_img(self, index):

        self.index = 0
        for cam in self.var_dict_["cam_folders"]:
            ## set the window location of images
            cv2.moveWindow( self.var_dict_["win_name"][self.index], 700, 500*self.index )
            ## set the window sizes
            cv2.resizeWindow(self.var_dict_["win_name"][self.index],\
                            self.var_dict_["win_dim"][1], self.var_dict_["win_dim"][0])
            ## mark the dictionary to grab img from
            tag = "bin_img_" + str(self.index + 1)
            ## grab dict and convert to unsigned int 8
            self.data_dict_[tag] = np.array ( self.data_dict_[tag], dtype = np.uint8)
            ## show the image
            cv2.imshow(self.var_dict_["win_name"][self.index], self.data_dict_[tag])

            ## end process
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            #time.sleep(0.005)

            ## histogram update process occurs here
            if index%20 == 0:

                ## grab intensity values
                tag = "int_" + str(self.index)
                self.cxs[self.index].set_xlim([0,850])
                self.cxs[self.index].set_ylim([0,8000])
                self.cxs[self.index].plot(self.x, self.data_dict_[tag])

                plt.draw()

            self.index += 1
        self.index = 0


if __name__ == '__main__':

    trials = ['trial_9_20_11']
    exe = img_proc(trials)
            
    for i in range(0,850):

        #exe.load_imgs(i)
        exe.load_bin(i)
        exe.proc_img(i)
        exe.view_img(i)
        
        
    
'''
self.hist, self.bins = np.histogram(img_array, bins=20)
self.center = (self.bins[:-1] + self.bins[1:]) / 2
x_low = min(self.bins)
x_high = max(self.bins)
print x_high
self.cxs[0].set_xlim( [x_low, x_high ] )
self.cxs[0].bar(self.center, self.hist)
'''
