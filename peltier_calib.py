import numpy as np
import os
from matplotlib import pyplot as plt

class main():

    def __init__(self, folder, start, cutoff):

        self.data_dict = {}
        self.var_dict = {}

        self.var_dict["voltages"] = ["0_5", "1_0", "1_5", "2_0", "2_5"] ## voltage in
        self.var_dict["peltier"] = ["b", "p"]   ## black and pink
        self.var_dict["board"] = ["d", "s"]   ## denver and spice
        self.var_dict["folder"] = folder
        self.var_dict["start"] = start
        self.var_dict["cutoff"] = cutoff
        self.var_dict["test"] = [ "denver", "spicer", "denver pink", "spicer pink" ]

    def load_data(self):

        os.chdir(self.var_dict["folder"])

        for gen in self.var_dict["peltier"]:
            for volt in self.var_dict["voltages"]:
                for board in self.var_dict["board"]:

                    tag = volt + "V_" + gen + board
                    ## only take time and temp
                    self.data_dict[tag] = np.genfromtxt(tag +".csv", delimiter = ",", \
                                                        usecols=(2,3), skip_header=(1))


    def plot_data(self):
        
        volt_index = 0
        for volt in self.var_dict["voltages"]:
            pelt_index = 0

            color_index = 0
            for gen in self.var_dict["peltier"]:
                colors = ["r", "b", "r--", "b--", "ro", 'bo']
                for board in self.var_dict["board"]:

                    tag = volt + "V_" + gen + board

                    test = self.var_dict["test"][color_index]

                    plt.figure(volt_index)
                    plt.plot( self.data_dict[tag][start:cutoff,0], self.data_dict[tag][start:cutoff,1], colors[color_index], label = test)
                    plt.title(volt)

                    print colors[color_index], tag, color_index, pelt_index

                    color_index += 1

                plt.legend( bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=len(self.var_dict["test"]), mode="expand", \
                            borderaxespad=0. )
                pelt_index += 1
            volt_index += 1

if __name__ == "__main__":

    folder = "./peltier_data"
    cutoff = 5 * 60
    start = 5 * 30
    exe = main(folder, start, cutoff)
    exe.load_data()
    exe.plot_data()
    plt.show()
