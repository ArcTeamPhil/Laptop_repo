#!/usr/bin/env python

import numpy as np
import os
import glob
import pandas
from matplotlib import pyplot as plt

class temp():

    def __init__(self):

        self.headers = [ "Index", "Day", "Date", "Temp 1", "Junk", "Temp 2"]
        self.headers = [ "Temp 1","Temp 2"]

        self.temps_ = {}


    def load(self):


        ## look for the excel file (assumes only one in directory)
        for file in os.listdir(os.getcwd()):
            if file.endswith("2_24.csv"):
                ## load the file
                data_df = pandas.read_csv(file, skip_blank_lines=True)

                ## drop NaN
                data_df.dropna(how='all', inplace=True)
                data_df.replace('', np.NaN, inplace=True)

                ## goes through every column loaded
                for column in data_df.columns:
                    print("column: ", column)

                    ## checks for match against user defined headers
                    if str(column) in self.headers:
                        ## adds the column contens to the dict ## 196609 is null
                        # self.temps_[column].replace('', np.NAN , inplace=True)
                        # self.temps_[column] = self.temps_[column][pandas.notnull(self.temps_[column])]

                        self.temps_[column] = np.array( (data_df[column][0:296719]), dtype = float)
                        print( self.temps_[column])
                        # not_blank = self.temps_[column] != ''

                        # self.temps_[column] = self.temps_[column][not_blank]
                        # print(self.temps_[column][50:65])

                        # if column in ["Temp 1", "Temp 2"]:
                        #     print( self.temps_[column][0:5])
                        #     self.temps_[column] = float(self.temps_[column])

    def norm(self):

        self.temps_["norm"] = self.temps_["Temp 1"] - self.temps_["Temp 2"]



    def plot(self, temp):

        plt.plot( self.temps_[temp])

if __name__ == "__main__":

    exe = temp()

    plt.figure()
    exe.load()
    exe.norm()
    exe.plot("Temp 1")
    exe.plot("Temp 2")
    exe.plot("norm")
    plt.show()


