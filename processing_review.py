import numpy as np
import os
from matplotlib import pyplot as plt

class proc_rev():

    def __init__(self, save_files):

        self.var_dict = {}
        self.var_dict["save_files"] = save_files
        self.var_dict["cutoff"] = 1200

        self.data_dict = {}

        self.fig, self.cxs = plt.subplots(len(save_files)/2,1, facecolor='w', edgecolor='k' )

    def load(self):

        for file in self.var_dict["save_files"]:

            path = os.getcwd()

            curr_file = path + '/' +  file

            print path

            self.data_dict[file] = np.genfromtxt(curr_file, usecols = 0, dtype = str)

            self.data_dict[file] = np.array ( self.data_dict[file], dtype = float)

            print max(self.data_dict[file])
    def plot(self):

        self.index = 0
        for file in  self.var_dict["save_files"]:

            cutoff = self.var _dict["cutoff"]
            time = np.linspace(0, len(self.data_dict[file])-cutoff, len(self.data_dict[file])-cutoff )
            
            self.cxs[int(self.index)].plot(time, self.data_dict[file][cutoff::] )
            self.cxs[int(self.index)].set_title(file[0:-6])

            self.index += 0.5


if __name__ == "__main__":

    save_files = [ 'trial_9_27_2_noise__mean_0', 'trial_9_27_2_noise__mean_1','trial_9_27_3_noise__mean_0','trial_9_27_3_noise__mean_1']
    exe = proc_rev(save_files)
    exe.load()
    exe.plot()
    plt.show()
