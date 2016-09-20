import numpy as np
import cv2
import os
from scipy import misc
import time
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

                array_16 = np.fromstring( image_str, np.uint16)

                self.data_dict_["buffer"] = np.append( self.data_dict_["buffer"], array_16 )

                if self.index == 0:
                    self.data_dict_["buffer"] = self.data_dict_["buffer"][2::]
                else:
                    pass

                ## in case of overflow case, start over with current file
                if len ( self.data_dict_["buffer"]) > 4920:

                    print "buffer overflow", len ( self.data_dict_["buffer"])
                    length = 4920
                    tag = "bin_img_" + str(self.index)


                    self.data_dict_[tag] = self.data_dict_["buffer"][0:length]
                    self.data_dict_["buffer"] = self.data_dict_["buffer"][length::]

                    print "buffer solved", len ( self.data_dict_[tag])

                    
                    self.data_dict_[tag] = np.reshape( self.data_dict_[tag], (60,82) )

                    self.data_dict_[tag] = self.data_dict_[tag][:, 2::]

                    print "image formed"
                else:
                    pass

                self.index += 1
            self.index = 0

    def view_img(self, index):

        for cam in self.var_dict_["cam_folders"]:

            cv2.moveWindow( self.var_dict_["win_name"][self.index], 500, 500*self.index )

            cv2.resizeWindow(self.var_dict_["win_name"][self.index],\
                            self.var_dict_["win_dim"][1], self.var_dict_["win_dim"][0])

            tag = "bin_img_" + str(self.index)
            cv2.imshow(self.var_dict_["win_name"][self.index], self.data_dict_[tag])

            ## end process
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.005)

            self.index += 1
        self.index = 0


if __name__ == '__main__':

    trials = ['trial_9_16_1']
    exe = img_proc(trials)

    for i in range(260,800):

        #exe.load_imgs(i)
        exe.load_bin(i)
        exe.view_img(i)
        
    
