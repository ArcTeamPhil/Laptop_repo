#!/usr/bin/env python

# import csv
import numpy as np
import os
import glob
import pandas

## delete first row of csv file
class data():

    def __init__(self):

        self.students_ = {}  ## store the student names to call dict

        self.var_dict_ = {}

        ## topics to look for and make into the pdf.
        ## the First Name and Last Name location should not be moved around
        ## the values in the block should be the exact same as in the CSV
        self.headers = [ "First Name",\
                         "Last Name",\
                         "Preferred Name to be Called / Nickname",\
                         "Home Street Address:",\
                         "E-Mail (this will be our main form of communication)",\
                         "School Name",\
                         "Why should you be selected for this program? (Not to exceed 2000 characters)",\
                         "Please list any extracurricular activities in which you participated for 2 years or more and the duration of involvement. This may include activities that you were involved with before high school IF your involvement continued into high school. (ex. Girl Scouts of America, 2009-2015)"]

    def load(self):

        ## look for the excel file (assumes only one in directory)
        for file in os.listdir(os.getcwd()):
            if file.endswith(".csv"):
                ## load the file
                data_df = pandas.read_csv(file)

                ## goes through every column loaded
                for column in data_df.columns:

                    ## checks for match against user defined headers
                    if str(column) in self.headers:
                        ## adds the column contens to the dict
                        self.students_[column] = data_df[column]


    def write(self):

        for i in range(len(self.students_[self.headers[0]])):
            ## create the markdown and pdf file names
            name_md = self.students_[self.headers[0]][i].strip() + "_" + self.students_[self.headers[1]][i].strip() + ".md"
            name_pdf = self.students_[self.headers[0]][i].strip() + "_" + self.students_[self.headers[1]][i].strip() + ".pdf"

            ## open the new markdown files
            file = open(name_md,'w')

            ## formatting
            # file.write("---")
            # file.write('\n\n')
            # file.write('\documentclass{article}')
            # file.write('\n\n')
            # file.write("---")
            # file.write('\n\n')


            ## iterate in sequential order through the headers
            for topic in self.headers:

                ## exception for name headers
                if topic in self.headers[0:3]:

                    if topic == self.headers[0]:
                        file.write('# ')
                    if topic == self.headers[2]:
                        file.write('_')
                    file.write(self.students_[topic][i])
                    if topic == self.headers[2]:
                        file.write('_ ')
                    file.write('\t\t')
                ## continue rest of doc with line for question
                else:
                    file.write('\n\n')
                    file.write('***')
                    file.write('\n\n')
                    file.write('## ' + topic)
                    file.write('\n\n')
                    file.write( self.students_[topic][i])
                    file.write('\n')

            file.close() 

            ## execute the pandoc conversion process
            command = "pandoc -r markdown -o " + name_pdf + " " + name_md
            print(command)
            os.system(command)

        ## show the user the results
        print("finished: completed files")
        os.system("ls -l | grep .pdf")


if __name__ == "__main__":

    exe = data()
    exe.load()
    exe.write()

