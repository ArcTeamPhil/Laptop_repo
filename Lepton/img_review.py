#!/usr/bin/env python

import numpy as np
import cv2
import os
from scipy import misc
import time
from matplotlib import pyplot as plt
import matplotlib.animation as animation
#import exifread


class data_extract():

    def __init__(self, trials, diff):

        os.chdir("/home/philrep")
        self.var_dict_ = {}
        self.var_dict_["trials"] = trials
        self.var_dict_["data_path"] = ''
        self.var_dict_["win_dim"] = [350, 500]
        self.var_dict_["win_name"] = [None]*len(trials)*2
        self.var_dict_["cam_folders"] = ['Lepton_1'] ##['Lepton_1/imgs/', 'Lepton_2/imgs/']
        self.var_dict_["bin_folders"] = ['Lepton_1'] ## ['Lepton_1/binary', 'Lepton_2/binary']
        self.var_dict_["img_roi"] = [[34,39], [40, 34] ] ##[[27,45], [29,41]] ##[[22, 47], [21,43]]##  ##[ [42,38], [42,34]] ##] ## ] 

        
        print self.var_dict_["win_name"]
        self.data_dict_ = {}
        self.data_dict_["buffer"] = np.zeros( (2),dtype=int)
        self.data_dict_["img_0"] = np.zeros( (60, 80), dtype = np.uint16)
        self.data_dict_["img_1"] = np.zeros( (60, 80), dtype = np.uint16)
        self.data_dict_["bin_img_0"] =  np.zeros( (60, 80), dtype = np.uint8)
        self.data_dict_["bin_img_1"] =  np.zeros( (60, 80), dtype = np.uint8)
        self.data_dict_["int_0"] = np.zeros( (diff), dtype = float)
        self.data_dict_["int_1"] = np.zeros( (diff), dtype = float)
        self.data_dict_["noise_0"] = np.zeros( (80*60/30), dtype = float)
        self.data_dict_["noise_1"] = np.zeros( (80*60/30), dtype = float)

        self.data_dict_["0"] = np.zeros( (60,80), dtype=np.uint8)
        self.data_dict_["0_color"] = np.zeros( (60,80,3), dtype=np.uint8)

        self.data_dict_["1"] = np.zeros( (60,80), dtype=np.uint8)
        self.data_dict_["1_color"] = np.zeros( (60,80,3), dtype=np.uint8)

        ## create windows for viewing images
        self.index = 0
        for i in range( len(self.var_dict_["win_name"]) ):
            self.var_dict_["win_name"][self.index] = 'window' + str(self.index)
            cv2.namedWindow( self.var_dict_["win_name"][self.index], cv2.WINDOW_NORMAL)
            self.index += 1
            
        self.index = 0
        self.radius = 3.0
        self.diff = diff

        ## plot histogram for images
        plt.ion()

        self.fig, self.cxs = plt.subplots(1,2, facecolor='w', edgecolor='k' )

        for i in range(2):
          self.cxs[i] = plt.gca()

          #self.cxs[i].set_ylim([0, 100])
          self.cxs[i].set_xlim([0,diff])


          self.x = np.linspace(0,diff, diff)
          tag = "int_" + str(i)
          self.cxs[i].plot( self.x, self.data_dict_[tag])


          ## get time history of average backgroun
          self.data_dict_["bck_grd_" +str(i)] = np.array( (1), dtype=float)

    def load_bin(self, index):

        self.index = 0
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
                #print bin_path
                ## open the file and read it
                f = open(bin_path, 'r')

                image_str = f.read()

                f.close()

                ## convert binary to unsigned 16 bit
                array_16 = np.fromstring( image_str, np.uint16)

                array_8 =  np.fromstring( image_str, np.uint16)

                array_8 /= 2.0**8

                array_8 = np.array(array_8, dtype=np.uint8)
                #print "max: ", np.max(array_16)
                array_8 = np.reshape(array_8, (60,82))

                array_8 = array_8[:,2::]
                ## preserve orgininal image contents 16 bit
                self.data_dict_["img_"+str(self.index)] = np.reshape(array_16, (60,82) )
                self.data_dict_["img_"+str(self.index)] = self.data_dict_["img_"+str(self.index)][:, 2::] 

                ## bring both images into same color contrast
                array_16 -= 10000


                roi = self.var_dict_["img_roi"][self.index]

                spacing = 2
                int_array = array_16[::30]
                intensity = np.sum(int_array)

                ## get a distrubution of the intensity of the img
                intensity /= (82*60/30)

                ## stack the intensity over time
                self.data_dict_["bck_grd_" +str(self.index)] = np.hstack(( self.data_dict_["bck_grd_" +str(self.index)], intensity))

                ## remove old data
                if len(self.data_dict_["bck_grd_" +str(self.index)]) > 30:
                    self.data_dict_["bck_grd_" +str(self.index)] = self.data_dict_["bck_grd_" +str(self.index)][1:30]



                ## use the median value for contrast
                avg_bck_grd = np.median(self.data_dict_["bck_grd_" +str(self.index)])

                #print intensity
                if self.index == 0:
                    low_equ = 6000
                    high_equ = 4000
                else:
                    low_equ = 1000
                    high_equ = 15000

                low_lim = avg_bck_grd - low_equ
                low_curve = np.where(array_16 <low_lim)
                high_lim = avg_bck_grd + high_equ
                if high_lim >= 2**16 -1:
                    high_lim = 2**16-1

                high_curve = np.where(array_16>high_lim)
                ##print "high: ",len (high_curve[0])
                ##print "low: ", len(low_curve[0])
                ## create modified version of raw data
                buffer = array_16
                buffer = np.array(buffer, dtype=float)
                ## bring all values above min to the floor
                buffer -= (2**16 - low_lim)
                ## normalize across the two limits
                buffer /= (high_lim-low_lim)
                ## bring them into 8 bit
                buffer *= 255.0


                ## set the limits to the extremes
                buffer[low_curve] = 0.0 #2.0**8
                buffer[high_curve] = 255.0

                ## print "bck grd intensity: ", low_lim, avg_bck_grd, high_lim 


                #buffer[32*80]
                ## set the tag mark for the dictionary
                tag = "bin_img_" + str(self.index)

                mask = np.ones((4920,), dtype = np.uint8)
                mask *= 255
                mask -= buffer

                self.data_dict_[tag] = np.reshape( mask, (60,82) )
                ## remove pre-info
                self.data_dict_[tag] = self.data_dict_[tag][:, 2::] ###
                self.data_dict_[str(self.index)] =np.array(array_8, dtype=np.uint8)##




                ## filter image
                self.data_dict_[tag] = np.array(self.data_dict_[tag], dtype=np.uint8)

                self.data_dict_[tag]= cv2.cvtColor(self.data_dict_[tag], cv2.COLOR_BAYER_GB2RGB)
                self.data_dict_[tag]= cv2.medianBlur(self.data_dict_[tag], 3)

                self.data_dict_[tag] = cv2.cvtColor(self.data_dict_[tag], cv2.COLOR_RGB2GRAY)


                self.index += 1
        self.index = 0
        

    def proc_img(self,index):

        self.index = 0
        for cam in self.var_dict_["bin_folders"]:

            roi = self.var_dict_["img_roi"][self.index]
            mask = np.zeros( (60,80), dtype=np.uint8)

            ## draw green (0,255,0) circle over nostril
            cv2.circle(mask,(roi[1], roi[0]), int(self.radius), 255,-1)
            max_div = np.sum(mask)/255.0
            focus = np.where( mask == 255)
            #print "focus: ", focus
            ## use the orgina limage 16 bit for processing
            int_array = self.data_dict_["img_"+str(self.index)][focus]
            #print int_array
            intensity = np.sum(int_array)
            intensity /= max_div

            ## print "obj intensity: ", intensity

            noise = self.data_dict_["img_"+str(self.index)]
            noise = np.reshape( noise, 80*60)
            noise = noise[::30]

            tag = "noise_" + str(self.index)
            self.data_dict_[tag] = noise

            tag = "int_" + str(self.index)
            self.data_dict_[tag][index] = intensity



            tag = "bin_img_" + str(self.index)
            cv2.circle(self.data_dict_[tag], (roi[1], roi[0]), int(self.radius), 255, 1)

            self.index += 1


    def view_img(self, index):

        self.index = 0
        for cam in self.var_dict_["cam_folders"]:
            ## set the window location of images
            #cv2.moveWindow( self.var_dict_["win_name"][self.index], 700, 500*self.index )
            ## set the window sizes
            # cv2.resizeWindow(self.var_dict_["win_name"][self.index],  self.var_dict_["win_dim"][1], self.var_dict_["win_dim"][0])
            ## mark the dictionary to grab img from
            tag = "bin_img_" + str(self.index)
            ## grab dict and convert to unsigned int 8
            self.data_dict_[tag] = np.array ( self.data_dict_[tag], dtype = np.uint8)
            ## show the image
            tag1 = str(self.index)
            image = self.data_dict_[tag1]
            # print "max: ", np.max(image)
            #image = np.copy(self.data_dict_[tag])
            image = cv2.applyColorMap(image, cv2.COLORMAP_JET)
            cv2.imshow(self.var_dict_["win_name"][self.index], image)

            self.data_dict_[str(self.index) + '_color'] = image

            ## end process
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            #time.sleep(0.005)

            self.index += 1
        self.index = 0


    def view_int(self, index):

        self.index = 0
        for cam in self.var_dict_["cam_folders"]:

            ## histogram update process occurs here
            if index%20 == 0:

                ## grab intensity values
                tag = "int_" + str(self.index)
                self.cxs[self.index].set_xlim([0,self.diff])
                #self.cxs[self.index].set_ylim([0,65000])

                self.cxs[self.index].plot(self.x, self.data_dict_[tag])

            
            self.index += 1
        plt.draw()

        self.index = 0

    def save_int(self, index,save_fold):

        self.index = 0
        for cam in self.var_dict_["cam_folders"]:
            
            tag = "int_" + str(self.index)
            prefix = save_fold + self.var_dict_["trials"][0]
            np.savetxt(prefix + "_" + tag, self.data_dict_[tag])
            self.index += 1

        self.index = 0

    def save_noise(self,index,save_fold):

        self.index = 0
        for cam in self.var_dict_["cam_folders"]:

            tag = "noise_" + str(self.index)
            prefix = save_fold + self.var_dict_["trials"][0]
            #np.savetxt(tag, self.data_dict_[tag])
            f = open(prefix + "_" + tag, 'a')
            np.savetxt( f, self.data_dict_[tag].reshape(1, self.data_dict_[tag].shape[0]), delimiter =','  )
            f.close()
            self.index += 1

        self.index = 0 

    def save_image(self,index,save_fold):

        self.index = 0
        for cam in self.var_dict_["cam_folders"]:

            tag = "image_" + str(self.index) +"_"+ "%08d" % index
            prefix = save_fold + self.var_dict_["trials"][0]
            #np.savetxt(tag, self.data_dict_[tag])
            #f = open(prefix + "_" + tag, 'a')
            tag = prefix+"_"+tag+".png"
            ## print(os.getcwd())
            print(tag)
            #cv2.imwrite(tag, self.data_dict_["bin_img_"+str(self.index)])
            cv2.imwrite(tag, self.data_dict_[str(self.index) + '_color'] )
            #np.savetxt( f, self.data_dict_[tag].reshape(1, self.data_dict_[tag].shape[0]), delimiter =','  )
            #f.close()
            self.index += 1

        self.index = 0 



        



if __name__ == '__main__':


    ## trial 2 is max 51593
    ## 15000 window reflcetion
    ## 18000 car
    ## 19000 car approach
    ## fridge 25000
    ## 31000 car again parked
    ## 34000 hot steam
    ## 43300 Car sequence begins
    ## 45500 car apssign
    ##47400 pav
    start = 14800 ## 19000 
    end = 15150 ##19260 ##53000 
    diff = end - start
    save_fold =  "Lepton_1/img_folder_6/" ##"trial_data/"
    trials = ['trial_11_25_2']
    exe = data_extract(trials, end)

    for i in range(start, end):
        
        exe.load_bin(i)
        exe.proc_img(i)
        exe.view_img(i)
        #exe.view_int(i)
        #exe.save_int(i,save_fold)
        #exe.save_noise(i,save_fold)
        exe.save_image(i,save_fold)

        
        
    
'''
'''
