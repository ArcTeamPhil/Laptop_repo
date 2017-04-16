#!/usr/bin/env python

# import csv
import numpy as np
import os
import glob
import pandas
import re

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
                         "Preferred Name:",\
                         "School Name",\
                         "City",\
                         "State",\
                         "Are you involved in a technology or engineering program during the regular school day or after school hours?", \
                         "If yes, please provide the name of the program and a brief description of activities that you have completed or will complete.",\
                         "What grade will you enter in the fall of 2016?",\
                         "Please list any STEM extracurricular activities (summer programs, clubs, etc.) in which you have participated or are participating and the duration of involvement. (ex. First Robotics, Sept 2013-June 2014)",\
                         "Please list any leadership roles that you have held or currently hold, the corresponding organization, and the duration of involvement. (ex. President, National Honors Society, Sept 2014-present)",\
                         "Please list any academic achievements and/or other honors and awards, the corresponding organization, and the year in which it was received. (ex. Female Scholar Athlete, School Athletics Department, 2014)",\
                         "Please list any extracurricular activities in which you participated for 2 years or more and the duration of involvement. This may include activities that you were involved with before high school IF your involvement continued into high school. (ex. Girl Scouts of America, 2009-2015)",\
                         "Please list all other extracurricular activities.",\
                         "If you listed any summer program(s) in any of the fields above, please give the name, location, and a brief description of the program(s).",\
                         "Why do you want to be an engineer?",\
                         "Describe a time when you worked in a team to solve a problem in class or an extracurricular activity. ",\
                         "Why should you be selected for this program? (Not to exceed 2000 characters)"
                         ]


    def load(self):

        ## look for the excel file (assumes only one in directory)
        for file in os.listdir(os.getcwd()):
            if file.endswith("generator.csv"):
                ## load the file
                data_df = pandas.read_csv(file)

                ## goes through every column loaded
                for column in data_df.columns:

                    ## checks for match against user defined headers
                    if str(column) in self.headers:
                        ## adds the column contens to the dict
                        self.students_[column] = data_df[column]


    def write(self):


        index = 0
        for i in range(len(self.students_[self.headers[0]])):
            # index += 1
            # if index >= 3:
            #     break
            ## create the markdown and pdf file names
            name_md = self.students_[self.headers[0]][i].strip() + "_" + self.students_[self.headers[1]][i].strip() + "_" + "Application" + ".md"
            name_pdf = self.students_[self.headers[0]][i].strip() + "_" + self.students_[self.headers[1]][i].strip() + "_" + "Application" + ".pdf"

            ## open the new markdown files
            file = open(name_md,'w')

            ## formatting


            ## iterate in sequential order through the headers
            for topic in self.headers:

                ## exception for name headers Last, First
                if topic in self.headers[0:2]:

                    if topic == self.headers[0]:

                        ## generate formatting 
                        file.write("---")
                        file.write('\n')
                        file.write("title: " + self.students_[topic][i].strip())
                        continue

                    else:
                        file.write("  " + self.students_[topic][i].strip())

                        file.write('\n')
                        file.write("fontsize: 11pt\n")
                        file.write("geometry: margin=1in\n")
                        file.write("header-includes:\n")
                        file.write("\t\t")
                        file.write("- \usepackage{textcomp}\n")
                        file.write("\t\t")
                        file.write("- \DeclareUnicodeCharacter{00A0}{ }\n")

                        file.write('output: pdf_document\n')
                        # file.write('\n\n')
                        file.write("---\n")
                        file.write('\sloppy\n')
                        # file.write('\n\n')


                        # file.write('\t\t')
                        continue

                ## excption for Preffered name
                if topic == self.headers[2]:

                    file.write('\n\n')
                    file.write('## ' + topic)
                    file.write(' _')
                    try:
                        file.write(self.students_[topic][i].strip())
                    except:
                        file.write("NA")
                    file.write('_ ')
                    file.write('\t\t')
                    continue

                ## excption for School name 
                if topic == self.headers[3]:
                    file.write('\n\n')
                    file.write('# ')
                    file.write(self.students_[topic][i].strip())
                    file.write('\t\t')
                    continue


                ## exception for city, state
                if topic in self.headers[4:6]:

                    ## city
                    if topic == self.headers[4]:
                        file.write('\n\n')
                        file.write('# ')
                        file.write(self.students_[topic][i].strip())
                        file.write(',\t\t')
                        continue

                    ## state
                    else:
                        file.write(self.students_[topic][i].strip())
                        file.write('\t\t')
                        continue

                ## continue rest of doc with line for question
                else:
                    # file.write('\n\n')
                    # file.write('***')
                    file.write('\n\n')
                    # print(topic)
                    file.write('## ' + topic)
                    file.write('\n\n')
                    try:
                        self.students_[topic][i] = re.sub('[\s+]',' ',self.students_[topic][i])
                        file.write( self.students_[topic][i].strip())
                    except:
                        file.write( "NA")
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

