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
        self.var_dict_["img_path"] = os.pardir
        self.var_dict_["win_dim"] = [350, 500]
        self.var_dict_["win_name"] = [None]*len(trials)*2
        self.var_dict_["cam_folders"] = ['Lepton_1_imgs', 'Lepton_2_imgs']

        print self.var_dict_["win_name"]
        self.data_dict_ = {}

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
            
            img_dir = os.path.abspath( os.path.join(self.var_dict_["img_path"], cam)) 

            
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
                cv2.moveWindow( self.var_dict_["win_name"][self.index], 500, 500*self.index )

                cv2.resizeWindow(self.var_dict_["win_name"][self.index],\
                                 self.var_dict_["win_dim"][1], self.var_dict_["win_dim"][0])

                cv2.imshow(self.var_dict_["win_name"][self.index], img)

                ## end process
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                time.sleep(0.005)


                self.index += 1
        self.index = 0

    def load_bin(self)

if __name__ == '__main__':

    trials = ['trial_9_16_1']
    exe = img_proc(trials)

    for i in range(260,800):

        exe.load_imgs(i)
        
    
