import numpy as np
import os
from matplotlib import pyplot as plt

class proc_rev():

    def __init__(self, save_files):

        self.var_dict = {}
        self.var_dict["save_files"] = save_files
        self.var_dict["cutoff"] = 0

        self.data_dict = {}

        self.fig, self.cxs = plt.subplots(len(save_files)/4 + 1,1, facecolor='w', edgecolor='k' )

    def load(self):

        for file in self.var_dict["save_files"]:

            path = os.getcwd()

            curr_file = path + '/' +  file

            print "path: ", path

            self.data_dict[file] = np.genfromtxt(curr_file, usecols = 0, dtype = str)

            self.data_dict[file] = np.array ( self.data_dict[file], dtype = float)

        ## take difference of intensity and noise floor
        for i in range(len(self.var_dict["save_files"]) / 2):

            diff_name = str(i)
            files = self.var_dict["save_files"]
            print files[i*2+1], "minus ", files[i*2]
            self.data_dict[diff_name] = abs(self.data_dict[files[i*2+1]] - self.data_dict[files[i*2]] )

    def plot(self):

        self.index = 0
        for file in  self.var_dict["save_files"]:

            cutoff = self.var_dict["cutoff"]
            time = np.linspace(0, len(self.data_dict[file])-cutoff, len(self.data_dict[file])-cutoff )
            
            self.cxs[int(self.index)].plot(time, self.data_dict[file][cutoff::] )
            self.cxs[int(self.index)].set_title(file[0:-6])
            #self.cxs[int(self.index)].set_yscale('log')
            
            #print file

            ## include the difference
            self.index += 0.25

        legend_name = [None]* (len(self.var_dict["save_files"]) / 2 )

        for i in range( len(self.var_dict["save_files"]) / 2):

            self.cxs[-1].plot(time, self.data_dict[str(i)][cutoff::] )

            legend_name[i] = str(i)


        print len(self.var_dict["save_files"])

        self.cxs[int(self.index)/2-1].legend(self.var_dict["save_files"][0:4])
        self.cxs[int(self.index)-1].legend(self.var_dict["save_files"][4::])
        self.cxs[-1].legend(legend_name)

if __name__ == "__main__":

    ## set trial names
    trials = [ '10_2_0', '10_2_1', '10_2_2']
    prefix = 'trial_'
    suffix_noise = '_noise__mean_'
    suffix_int = '_int_'

    save_files = [None]*len(trials)*4

    index = 0
    for trial in trials:

        for i in range(2):
            save_files[index] = prefix + trial + suffix_noise + str(i)
            index += 1
            save_files[index] = prefix + trial + suffix_int + str(i)
            index += 1
    #print save_files

    #save_files = [ 'trial_10_2_2_noise__mean_0', 'trial_10_2_2_noise__mean_1','trial_10_2_2_int_0', 'trial_10_2_2_int_1','trial_10_1_2_noise__mean_0','trial_10_1_2_noise__mean_1','trial_10_1_2_int_0', 'trial_10_1_2_int_1']
    #print save_files

    exe = proc_rev(save_files)
    exe.load()
    exe.plot()
    plt.show()

