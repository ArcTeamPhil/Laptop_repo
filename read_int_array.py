


import numpy as np
import cv2
import time

cv2.namedWindow('window_1', cv2.WINDOW_NORMAL)
#x = np.load('test_array')

img_array = np.genfromtxt('int_array_1.txt', delimiter='\t', skip_header=1, \
                       skip_footer=0, usecols=0, dtype=float)

## find 30 placeholder
img_ints = img_array

print "image ints: ", img_ints[0:10]


## search for the last row in every image
int_start =  np.where( img_ints == 20 )
## seperate the array of indeices
int_start = int_start[0]
## add 82 to get to the first row of the next image
int_start = int_start 

print "image starters: ", int_start[0:10]
print "starter vlaues: ", img_ints [ int_start[0:10]]
print " images: ", len(int_start)





img = np.zeros( (60, 80), dtype = np.uint8)

'''
while(1):

    
    for j in range(0, len(int_start) ):

        img = np.array( (img), dtype =np.uint8)

        #print "image: ", j
        #print "image index : ", int_start[j]
        img_len =   int_start[j+1] - int_start[j]
        print "length: ", img_len
        ## check for all data tranmission length
        ## 4920 is complete image
        if img_len != 4920:
            continue

        for i in range(60):

            index = int_start[j] + i*82 + 2

            img[i,:] = img_ints[index: index + 80]
            #print img_ints[index:index +10]


       
        time.sleep(0.05)
        name = 'img_' + str(j) + '.png'

        #img[30:40,30:40] = 40

        #cv2.imwrite(name, img)



        cv2.imshow('window_1', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
'''



