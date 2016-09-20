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
        
        print self.var_dict_["win_name"]
        self.data_dict_ = {}
        self.data_dict_["buffer"] = np.zeros( (2),dtype=int)
        self.data_dict_["img_0"] = np.zeros( (60, 80), dtype = np.uint8)
        self.data_dict_["img_1"] = np.zeros( (60, 80), dtype = np.uint8)
        self.data_dict_["bin_img_0"] =  np.zeros( (60, 80), dtype = np.uint16)
        self.data_dict_["bin_img_1"] =  np.zeros( (60, 80), dtype = np.uint16)


        ## create windows for viewing images
        self.index = 0
        for i in range( len(self.var_dict_["win_name"]) ):
            self.var_dict_["win_name"][self.index] = 'window' + str(self.index)
            cv2.namedWindow( self.var_dict_["win_name"][self.index], cv2.WINDOW_NORMAL)
            self.index += 1
            
        self.index = 0

        ## plot histogram for images
        plt.ion()
        fig = plt.figure()
        ## ax = fig.add_subplot(111)
        self.ax = plt.gca()
        self.ax.set_ylim(0, 1500 )

        x = np.linspace(0,256, 100)

        self.hist, self.bins = np.histogram(x, bins=20)

        self.center = (self.bins[:-1] + self.bins[1:]) / 2
        self.ax.bar(self.center, self.hist) 
        ## self.line2, = ax.plot(time_series, resp_chart_filt, 'r-', linewidth = 5.0)


        for key in self.var_dict_:
            print self.var_dict_[key]

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

                bin_path = os.path.join(bin_dir, j)
                first_trial = os.listdir(bin_path)[0]
                bin_base = str(first_trial)
                base_len = bin_base.rfind('_')
                bin_base = bin_base[0:base_len+1]


                file_len = len( os.listdir(bin_path))


                bin_name = bin_base + str(index) + '.txt'
                
                bin_path = os.path.join(bin_path, bin_name)

                f = open(bin_path, 'r')

                image_str = f.read()

                f.close()
                tag = "bin_img_" + str(self.index + 1)

                buffer = np.fromstring( image_str, np.uint16)
                
                buffer = buffer /2**8

                
                self.data_dict_["buffer"] = np.ones(len(buffer), dtype = np.uint8)*256

                self.data_dict_["buffer"] = self.data_dict_["buffer"] - buffer

                self.data_dict_[tag] = np.reshape( self.data_dict_["buffer"], (60,82) )

                self.data_dict_[tag] = self.data_dict_[tag][:, 2::]



                self.index += 1
        self.index = 0
            
    def view_img(self, index):

        self.index = 0
        for cam in self.var_dict_["cam_folders"]:

            cv2.moveWindow( self.var_dict_["win_name"][self.index], 500, 500*self.index )

            cv2.resizeWindow(self.var_dict_["win_name"][self.index],\
                            self.var_dict_["win_dim"][1], self.var_dict_["win_dim"][0])

            tag = "bin_img_" + str(self.index + 1)

            self.data_dict_[tag] = np.array ( self.data_dict_[tag], dtype = np.uint8)
            cv2.imshow(self.var_dict_["win_name"][self.index], self.data_dict_[tag])

            ## end process
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            #time.sleep(0.005)

            if self.index == 0 and index%10 == 0:
              img_array = np.reshape(  self.data_dict_[tag], (60*80) )
              self.hist, self.bins = np.histogram(img_array, bins=20)
              self.center = (self.bins[:-1] + self.bins[1:]) / 2
              plt.xlim(min(self.bins), max(self.bins))
              self.ax.bar(self.center, self.hist) 
              plt.draw()

            self.index += 1
        self.index = 0


if __name__ == '__main__':

    trials = ['trial_9_20_0']
    exe = img_proc(trials)

    for i in range(260,800):

        #exe.load_imgs(i)
        exe.load_bin(i)
        exe.view_img(i)
        
    
