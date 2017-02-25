#!/usr/bin/env python

## notes

##
'''
## http://ac.els-cdn.com/S0034425707000454/1-s2.0-S0034425707000454-main.pdf?_tid=b7c6c170-f6cf-11e6-b3a4-00000aacb361&acdnat=1487528448_605885776ff4712c91db5d3f07810314
DHR against cumbled aluminum foil bc of high reflectivity (0.93) [pg3]
Pllants have high Emissivity (0.9 >)
Spectral radiance entering calibrated with blackbody targets in scene 10 and 40 C

Measurements were divided by blackbody at same temp
** temp of plant is unknown
**** used sample at ambiant temp
'''
import numpy as np
from matplotlib import pyplot as plt

class theory():

    def __init__(self):

        self.data_dict_ = {}
        ## B_lamb [ W * sr-1 * m-3]
        self.h = 6.626e-34 ## [J*s]lanls constant
        self.c = 2.99e8 ## speed of light
        self.length_L = 1000  ## vector length lemabda
        self.length_T = 2 #11  ## vector length temperatures
        self.T = np.linspace( 25+274.1 , 35+274.1, num=self.length_T )
        self.lamb = np.linspace( 4e-6, 15e-6, num=self.length_L) ## [m]
        self.k = 1.380e-23 ## [J*K-1]Boltzman const
        self.b = 2900  ## um * K constant of proportionality
        # self.emis = np.array( (0.98, 0.75, 0.5, 0.1) )

        self.emis = np.array( (1.01, 1.00, 0.99, 0.98, 0.97, 0.96, 0.95) )

        ## for blackbody confirmation check
        # self.emis = np.array( (1.0 ,1.0) )
        # self.lamb = np.linspace( 0.2e-6, 2e-6, num=self.length_L) ## [m]
        # self.T = np.linspace( 4000 , 5000, num=self.length_T )

        self.height = np.array( (0.2, 0.4, 0.6, 0.8, 1.0) )
        self.lens_r = 0.0005 ## len rad = 0.5 mm

    def build_dict(self):

        for j in range( len(self.emis) ):

            dict_key = 'B_lamb_' + str(self.emis[j])
            dict_key_max = 'lamb_max_' + str(self.emis[j])

            self.data_dict_[dict_key] =  np.zeros( (self.length_T,self.length_L) ,dtype=float)
            self.data_dict_[dict_key_max] = np.zeros( (self.length_T,2) ,dtype=float)




    def planck_rad(self):

        ## https://en.wikipedia.org/wiki/Planck%27s_law

        for j in range( len(self.emis) ):

            for i in range(self.length_T):

                dict_key = 'B_lamb_' + str(self.emis[j])

                ## solve for spectral desnity of em radiation 
                self.data_dict_[ dict_key ][i,:] = \
                                            self.emis[j] * (2 * self.h * self.c**2 / \
                                                                      self.lamb**5 ) * \
                                             1 / \
                                             ( np.e**( \
                                                       (self.h * self.c) / \
                                                       (self.lamb * self.k * self.T[i] ) \
                                                     ) -1 )

                dict_key_max = 'lamb_max_' + str(self.emis[j])

                max_L = np.max( self.data_dict_[ dict_key][i,:] )
                ind_max = np.argmax( self.data_dict_[ dict_key ][i,:] )

                self.data_dict_[dict_key_max][i] =\
                                        np.array ( ( max_L, ind_max), dtype=float)




    def cam_irrad(self):

        for j in range( len(self.height) ):

            theta = np.arctan(self.lens_r / self.height[j]) ## rad
            ster = 2 * np.pi * ( 1- np.cos(theta) )
            print("ster: ", ster)



    def plot_spectral(self):

        plt.figure()

        for j in range( len(self.emis) ):
            for i in range(self.length_T):

                dict_key_max = 'lamb_max_' + str(self.emis[j])

                ind_max = self.data_dict_[ dict_key_max ][i,1]
                max_L = self.data_dict_[ dict_key_max ][i,0]

                lamb_max = self.lamb[ ind_max ] *10**6 ## um
                spec_max = max_L/1e12  ## kW * sr-1 * m-2 * um-1

                dict_key = 'B_lamb_' + str(self.emis[j])

                lamb = self.lamb*10**6
                spec_rad = self.data_dict_[ dict_key ][i,:] /1e12 ## kW*sr-1*m-2*um-1

                plt.plot(lamb_max , spec_max, 'o')
                plt.plot(lamb , spec_rad , "--", label=str(self.T[i]-274.1) + '_' + str(self.emis[j] ) )

        plt.legend()
        plt.show()

if __name__ == "__main__":

    exe = theory()
    exe.build_dict()
    exe.planck_rad()
    exe.plot_spectral()

    #exe.cam_irrad()



