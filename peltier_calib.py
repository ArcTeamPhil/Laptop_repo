import numpy as np
import os
from matplotlib import pyplot as plt

class main():

    def __init__(self, folder, start, cutoff):

        self.data_dict = {}
        self.var_dict = {}

        self.var_dict["voltages"] = [ "1_0", "1_5", "2_0", "2_5", "3_0"] ## voltage in
        self.var_dict["peltier"] = ["b", "p"]   ## black and pink
        self.var_dict["board"] = ["d", "s"]   ## denver and spice
        self.var_dict["cooling"] = ["nofan", "fan"]  ## on or off fan cooling
        self.var_dict["folder"] = folder
        self.var_dict["start"] = start
        self.var_dict["cutoff"] = cutoff
        self.var_dict["test"] = [ "denver black nofan", "spicer black nofan", "denver pink nofan", "spicer pink nofan", \
        "denver black fan", "spicer black fan", "denver pink fan", "spicer pink fan",]

    def load_data(self):

        os.chdir(self.var_dict["folder"])

        for gen in self.var_dict["peltier"]:
            for volt in self.var_dict["voltages"]:
                for board in self.var_dict["board"]:
                    for cool in self.var_dict["cooling"]:

                        tag = volt + "_" + gen + board + '_' + cool
                        ## only take time and temp
                        self.data_dict[tag] = np.genfromtxt(tag +".csv", delimiter = ",", \
                                                            usecols=(2,3), skip_header=(1)) ## 45 hot, 23 cold


    def plot_data(self):
        
        volt_index = 0
        for volt in self.var_dict["voltages"]:
            pelt_index = 0

            color_index = 0
            for gen in self.var_dict["peltier"]:
                colors = [ "k", 'k--', '*k', '*k--', "m", "m--", "*m", "*m--"]
                for board in self.var_dict["board"]:

                    for cool in self.var_dict["cooling"]:

                        tag = volt + "_" + gen + board + '_' + cool

                        test = self.var_dict["test"][color_index]

                        plt.figure(volt_index)
                        x = self.data_dict[tag][::20,0]

                        y = self.data_dict[tag][::20,1]
                        plt.plot(x[start/20:cutoff/20],  y[start/20:cutoff/20], colors[color_index], label = tag)
                        plt.title(volt)

                        print colors[color_index], tag, color_index, pelt_index

                        color_index += 1

                plt.legend( bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=len(self.var_dict["test"])/2, mode="expand", \
                            borderaxespad=0. )
                pelt_index += 1
            volt_index += 1

if __name__ == "__main__":

    folder = "./peltier_data_2"
    cutoff = 5 * 180
    start = 0 ##5 * 30
    exe = main(folder, start, cutoff)
    exe.load_data()
    exe.plot_data()
    plt.show()
