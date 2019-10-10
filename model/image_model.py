from skimage import io
from skimage import filters, color
from skimage import transform
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import numpy as np
import os
import fnmatch
from sklearn import neighbors
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from skimage.morphology import skeletonize


def dir2filename(dirName):
    # read files from directory
    matches = []
    for root, dirnames, filenames in os.walk(dirName):
        for filename in fnmatch.filter(filenames, '*.[jp]*'):
            matches.append(os.path.join(root,filename))

    return matches

def add_padding(img, pad_l, pad_t, pad_r, pad_b):
    height, width = img.shape
    #Adding padding to the left side.
    pad_left = np.zeros((height, pad_l), dtype = np.int)
    img = np.concatenate((pad_left, img), axis = 1)
    
    #Adding padding to the top.
    pad_up = np.zeros((pad_t, pad_l + width))
    img = np.concatenate((pad_up, img), axis = 0)
    
    #Adding padding to the right.
    pad_right = np.zeros((height + pad_t, pad_r))
    img = np.concatenate((img, pad_right), axis = 1)
    
    #Adding padding to the bottom
    pad_bottom = np.zeros((pad_b, pad_l + width + pad_r))
    img = np.concatenate((img, pad_bottom), axis = 0)
    
    return img

def img2fv(fileName, digit_fv, row, col):
    
    digit_y = fileName.split('/')[-1].split('__')[0]
    digit_x = np.zeros((1,(row*col)), dtype='float64')
    #print(digit_y)
    digit = io.imread(fileName)
    gray_image = color.rgb2gray(digit)
    gray_image = gray_image < 0.95
    gray_image = gray_image[:,:col]
    
    ### Attempt to skeletonize to improve performance
    
    #gray_image = skeletonize(gray_image)
    #gray_image = convex_hull_image(gray_image)
    #print(gray_image.shape)
    #io.imshow(gray_image)
    #io.show()
    
    
    ### Attempt to shift the image to top-left corner
    """
    col_sum = np.where(np.sum(gray_image, axis = 0)>1)
    row_sum = np.where(np.sum(gray_image, axis = 1)>1)
    if row_sum[0].size != 0 and col_sum[0].size != 0:
        y1= row_sum[0][0]
        x1= col_sum[0][0]
    #print x1, y1
    #print x2, y2
        gray_image = add_padding(gray_image[y1:,x1:], 0, 0, x1, y1)
    #io.imshow(gray_image)
    #io.show()
    """
    
    #print(gray_image.shape)
    
    digit_x = transform.resize(gray_image, (row,col), mode='reflect')
    digit_x = digit_x.reshape((1,(row*col)))
    tmp_digit_data = np.hstack((digit_y, digit_x[0,:]))
    digit_fv = np.vstack((digit_fv, tmp_digit_data))
    return digit_fv

dirName = 'images'
matches = dir2filename(dirName)
matches.sort()
row = 56
col = 62
digit_fv = np.zeros((1,(row*col)+1), dtype='float64')

for i in range(0, 2000):
    digit_fv = img2fv(matches[i],digit_fv, row, col)


# remove first row
digit_fv = np.delete(digit_fv, 0, 0)


digit_data = digit_fv
X = digit_data[:,1:]
y = digit_data[:,0]

kf = KFold(n_splits=50,random_state=10,shuffle=True)
accuracies = []
for train_index, test_index in kf.split(X):
    #print("TRAIN:", train_index, "TEST:", test_index)
    data_train   = X[train_index]
    target_train = y[train_index]
    
    data_test    = X[test_index]
    target_test  = y[test_index]
    
    KNN = neighbors.KNeighborsClassifier(n_neighbors=10, weights='distance')
    KNN.fit(data_train,target_train)
    
    preds = KNN.predict(data_test)
    
    accuracy = accuracy_score(target_test,preds)
    accuracies.append(accuracy)

# this is the average accuracy over all folds
average_accuracy = np.mean(accuracies)
print("average_accuracy")
print(average_accuracy)

