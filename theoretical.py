#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt

class theory():

    def __init__(self):

        self.data_dict_ = {}
        self.length_L = 1000  ## vector length
        self.length_T = 10  ## vector length
        self.h = 6.626e-34 ## [J*s]lanls constant
        self.c = 2.99e8 ## speed of light
        # self.T = np.linspace( 25+274.1 , 35+274.1, num=self.length_T )
        self.T = np.linspace( 4000 , 5000, num=self.length_T )
        self.k = 1.380e-23 ## [J*K-1]Boltzman const
        self.b = 2900  ## um * K constant of proportionality
        # self.emis = np.array( (0.98, 0.75, 0.5, 0.1) )
        self.emis = np.array( (1.0 ,1.0) )
        self.lamb = np.linspace( 0.2e-6, 2e-6, num=self.length_L) ## [m]
        ## B_lamb [ W * sr-1 * m-3]

    def build_dict(self):

        for i in range( len(self.emis) ):
            self.data_dict_['B_lamb_' + str(self.emis[i]) ] =  np.zeros( (self.length_T,self.length_L) ,dtype=float)
        # B_lamb = np.zeros( (self.length_T,self.length_L) ,dtype=float)
            self.data_dict_['self.lamb_max_' + str(self.emis[i])] = np.zeros( (self.length_T,2) ,dtype=float)




    def plank(self):

        ## https://en.wikipedia.org/wiki/Planck%27s_law

        for j in range( len(self.emis) ):

            for i in range(self.length_T):

                dict_key = 'B_lamb_' + str(self.emis[j])

                self.data_dict_[ dict_key ][i,:] = \
                                            self.emis[j] * (2 * self.h * self.c**2 / \
                                                                      self.lamb**5 ) * \
                                             1 / \
                                             ( np.e**( \
                                                       (self.h * self.c) / \
                                                       (self.lamb * self.k * self.T[i] ) \
                                                     ) -1 )

                max_L = np.max( self.data_dict_[ dict_key][i,:] )
                ind_max = np.argmax( self.data_dict_[ dict_key ][i,:] )

                self.data_dict_['self.lamb_max_' + str(self.emis[j])][i] =\
                                        np.array ( ( max_L, ind_max), dtype=float)





    def plot(self):

        plt.figure()

        for j in range( len(self.emis) ):
            for i in range(self.length_T):

                dict_key_max = 'self.lamb_max_' + str(self.emis[j])

                ind_max = self.data_dict_[ dict_key_max ][i,1]
                max_L = self.data_dict_[ dict_key_max ][i,0]

                lamb_max = self.lamb[ ind_max ] *10**6 ## um
                spec_max = max_L/1e12  ## kW * sr-1 * m-2 * um-1

                dict_key = 'B_lamb_' + str(self.emis[j])

                lamb = self.lamb*10**6
                spec_rad = self.data_dict_[ dict_key ][i,:] /1e12 ## kW*sr-1*m-2*um-1

                plt.plot(lamb_max , spec_max, 'o')
                plt.plot(lamb , spec_rad , "--", label=self.T[i])

        plt.legend()
        plt.show()

if __name__ == "__main__":

    exe = theory()
    exe.build_dict()
    exe.plank()
    exe.plot()

