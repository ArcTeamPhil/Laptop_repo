


import numpy as np
import cv2
import time

print "\n"

cv2.namedWindow('window_1', cv2.WINDOW_NORMAL)
#x = np.load('test_array')


img_array = np.genfromtxt('./Lepton_1/test_13_56.txt', delimiter='\t', skip_header=1, skip_footer=0, usecols=0, dtype=float)

## find 30 placeholder
thirty = np.where(img_array == 30)
print "where thirties: ", thirty[0]

start_thirty = thirty[0][0]

print "total length: ", len(img_array)
print "thirties: ", len(thirty[0])

thirty_repeat = thirty[0][1::] - thirty[0][0:-1]
not_thirty_repeat =  np.where(thirty_repeat != 2)[0]
print "how many not thirty: ", len(not_thirty_repeat)
print "not step thirty: ", not_thirty_repeat
not_thirty_step =  thirty_repeat[not_thirty_repeat]
print "how big step: ", not_thirty_step

print "first row: ", not_thirty_repeat[0]
print "data_index: ", thirty[0][not_thirty_repeat[0]]

print img_array[ thirty[0][not_thirty_repeat[0]]-3: thirty[0][not_thirty_repeat[0]]+3]

print" imge row"
print not_thirty_repeat[0]+not_thirty_step[0]

not_thirty_diff = not_thirty_repeat[1::] - not_thirty_repeat[0:-1]
print "not thirty diff: ", not_thirty_diff



prev_index = 0
for j in range(15,23):
    print "where is : ",j,   np.where( img_array == j)[0]

img = np.zeros( ( 60,80), dtype=np.uint8)
############ row isolation ###########
img_start = not_thirty_repeat[0]*2 + 4

thirty = thirty[0]
if thirty[0] > 1:
    img_start += thirty[0]-1
else:
    pass
print "img start: ", img_start
for i in range(32): ##len(not_thirty_repeat)-2):

    print "prev difference: ", not_thirty_diff[i]
    print
    if not_thirty_diff[i] >= 80 and not_thirty_diff[i] < 82:
        if i > 0:
            guess = img_start + 164
        else:
            guess = img_start
    elif not_thirty_diff[i] == 1:
        continue
    else:
        guess = img_start + (not_thirty_diff[i]+2 ) * 2
        print "################################# short: ", not_thirty_diff[i]

   
    print "guess   : ", img_array[ guess-5: guess +5 ], img_array[guess]  ## expt 26*2  56
    data_half = img_array[guess::2]
    img_row = data_half[1:81]
    img_row = np.array( (img_row), dtype=np.uint8)
    row_index = img_array[guess]
    if row_index > 60:
        pass
    else:
        img[row_index,:] = img_row

    img_start = guess
    cv2.imshow('window_1', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

time.sleep(2)
#img = np.zeros( (60, 80), dtype = np.uint8)

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

        cv2.imwrite(name, img)



        cv2.imshow('window_1', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
'''




