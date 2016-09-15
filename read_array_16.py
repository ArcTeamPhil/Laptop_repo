


import numpy as np
import cv2
import time
from matplotlib import pyplot as plt
print "\n"

cv2.namedWindow('window_1', cv2.WINDOW_NORMAL)
#x = np.load('test_array')

test = str(28)
buffer = np.zeros( (2),dtype=int)
print "\n"
index_start = 52
for j in range(index_start,750):
    
    #print "\n new image" + str(j) + " \n"
    file = './Lepton_1/test_'+test+'/test_'+test+'_' + str(j) + '.txt'
    #img_array = np.genfromtxt(file, delimiter='\n', skip_header=1, skip_footer=0, usecols=0, dtype=np.uint8)

    f = open(file, "r")
    array_8 = f.read()
    #img_array = img_bytes.astype(np.uint8)

    #img_array = np.fromfile(f, dtype=np.uint8)

    #array_8 = np.fromstring(array_8, dtype=np.uint8)
    f.close()
    f = open(file, "r")
    array_16 = f.read()
    array_16 = np.fromstring(array_16, dtype=np.uint16)
    f.close()
    print "len 8: ", len(array_8), "len 16: ", len(array_16)
    buffer = np.append(buffer, array_16)

    if j - index_start == 0:
        print "subtraction"
        
        buffer = buffer[2::]
    
    print "buffer len: ", len(buffer)

    if len(buffer) > 4920:
        buffer = array_16
    elif len(buffer) == 4920:
        print "##########"

        img_array = np.reshape(buffer, (60,82))
        img_array = img_array[:, 2::]
        print img_array.shape


        min = np.min(img_array)*1.0
        max = np.max(img_array)*1.0
        print "min, max: ", min, max
        median = np.median(img_array)
        print "median: ", median
        print "div: ", (max-min)
        "buffer start: ", buffer[0:5]
        img_array /= min / 30.0
        #img_array *= 256.0
        print "new max: ", np.max(img_array)*1.0
        print img_array[0:5,0]
        #img_array = np.array( img_array, dtype=np.uint8)
        print "array img: ", img_array[0:5,0]

        cv2.imshow('window_1',img_array)
        time.sleep(0.05)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    else:
        pass

    #print "diff: ", len(img_array) - 60.0*80.0
    
    #print "shortened array: ", len(new_array)
    #print len(new_array)/60.0
    #print img_array[diff-5:diff+5]

    '''
    new_array = new_array.reshape(60,80)
    min = np.min(new_array)
    max = np.max(new_array)
    #print min
    scale = (max-min)*256

    new_array *= scale

    new_array = np.array( new_array, dtype=np.uint8)
    cv2.imshow('window_1',new_array)
    #time.sleep(0.5)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    f.close()
    
    
    plt.figure()
    plt.imshow(new_array)
    plt.show()
    '''




