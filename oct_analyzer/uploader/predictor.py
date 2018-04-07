
import keras
from keras.layers import Activation
from keras.layers import Conv2D, MaxPooling2D, Deconvolution2D
from keras.models import Model
from keras.layers import Input
from keras.layers import BatchNormalization
from keras.layers import UpSampling2D
from keras.layers import Concatenate
from keras.layers import Lambda,Add 
from keras.utils import to_categorical
import tensorflow as tf

from keras.layers import Reshape

from keras import backend as K
from keras import regularizers, optimizers

import scipy.io as scio
import numpy as np    
import os
import matplotlib.pyplot as plt
import math
from scipy.misc import imsave
from scipy import ndimage, misc
from numpy import unravel_index
from operator import sub
import re
#from django.conf import settings

def predict(path,results_path,name):
    data_shape = 216*64
    weight_decay = 0.001

    inputs = Input(shape=(216,64,1))

    L1 = Conv2D(64,kernel_size=(3,3),padding = "same",kernel_regularizer=regularizers.l2(weight_decay))(inputs)
    L2 = BatchNormalization()(L1)
    L2 = Activation('relu')(L2)
    L3 = MaxPooling2D(pool_size=(2,2))(L2)
    L4 = Conv2D(128,kernel_size=(3,3),padding = "same",kernel_regularizer=regularizers.l2(weight_decay))(L3)
    L5 = BatchNormalization()(L4)
    L5 = Activation('relu')(L5)
    L6 = MaxPooling2D(pool_size=(2,2))(L5)
    L7 = Conv2D(128,kernel_size=(3,3),padding = "same",kernel_regularizer=regularizers.l2(weight_decay))(L6)
    L8 = BatchNormalization()(L7)
    L9 = Activation('relu')(L8)
    L10 = Conv2D(128,(3,3),dilation_rate= (2,2), padding = "same", activation='relu', name = "conv_dil_1")(L9)
    L11 = BatchNormalization()(L10)
    L12 = Activation('relu')(L11)
    L13 = Conv2D(128,(3,3),dilation_rate= (4,4), padding = "same", activation='relu', name = "conv_dil_2")(L12)
    L14 = BatchNormalization()(L13)
    L15 = Activation('relu')(L14)
    L16 = Conv2D(128,(3,3),dilation_rate= (8,8), padding = "same", activation='relu', name = "conv_dil_3")(L15)
    L17 = BatchNormalization()(L16)
    L18 = Activation('relu')(L17)
    L19 = Conv2D(128,kernel_size=(3,3),padding = "same",kernel_regularizer=regularizers.l2(weight_decay),
                name="skip_conv_1")(L6)
    L19 = BatchNormalization()(L19)
    L19 = Activation('relu')(L19)
    L20 = Add()([L18,L19])
    L21 = UpSampling2D( size = (2,2)) (L20)
    L21 = Conv2D(128,(3,3), padding = "same", kernel_regularizer=regularizers.l2(weight_decay))(L21)
    L22 = BatchNormalization()(L21)
    L23 = Activation('relu')(L22)
    L24 = Conv2D(128,kernel_size=(3,3),padding = "same",kernel_regularizer=regularizers.l2(weight_decay),
                name="skip_conv_2")(L3)
    L24 = BatchNormalization()(L24)
    L24 = Activation('relu')(L24)
    L24 = Add()([L23,L24])
    L25 = UpSampling2D(size = (2,2))(L24)
    L25 = Conv2D(64, (3,3), padding = "same", kernel_regularizer=regularizers.l2(weight_decay))(L25) 
    L26 = BatchNormalization()(L25)
    L27 = Activation('relu')(L26)
    L28 = Conv2D(8,kernel_size=(1,1),padding = "same",kernel_regularizer=regularizers.l2(weight_decay))(L27)
    L29 = Reshape((data_shape,8),input_shape = (216,64,8))(L28)
    L30 = Activation('softmax')(L29)
    model = Model(inputs = inputs, outputs = L30)

    model.load_weights("/home/prajwala/Videos/oct_analyzer/uploader/weights.hdf5")
    #model.load_weights(settings.STATIC_PATH+"weights.hdf5")
    image = ndimage.imread(path)
    final_image = np.zeros((216,448,3))
    temporary = []
    #print("Type of image is ")
    #print(image.dtype)
    for temp in range(7):
        image_resized = image[:,64*temp:(64*(temp+1))]
        testing = image_resized.reshape((1,216,64,1))
        prediction = model.predict(testing)
        predicted_reshaped = prediction.reshape((216,64,8))
        output = np.zeros((216,64))
        for i in range(216):
            for j in range(64):
                index = np.argmax(predicted_reshaped[i][j])
                output[i][j] = index
        color= np.zeros((216,64,3))
        c0 = 0
        c1 = 0
        c2 = 0
        c3 = 0
        c4 = 0
        c5 = 0
        c6 = 0
        c7 = 0
        j = 0
        for j in range(216):
            for k in range(64):
                if(output[j][k]==0):
                    c0 = c0 + 1
                    color[j][k] = [0,0,0]
                if(output[j][k]==1):
                    c1 = c1 + 1
                    color[j][k] = [128,0,0]
                if(output[j][k]==2):
                    c2 = c2 + 1
                    color[j][k] = [0,128,0]
                if(output[j][k]==3):
                    c3 = c3 + 1
                    color[j][k] = [128,128,0] 
                if(output[j][k]==4):
                    c4 = c4 + 1
                    color[j][k] = [0,128,128]
                if(output[j][k]==5):
                    c5 = c5 + 1
                    color[j][k] = [64,0,0]
                if(output[j][k]==6):
                    c6 = c6 + 1
                    color[j][k] = [192,0,0]
                if(output[j][k]==7):
                    c7 = c7 + 1
                    color[j][k] = [64,128,0]
        temp = final_image[:,(64*temp):(64*(temp+1)),:]
        temp = color
        temporary.append(temp)
    
    for i in range(7):
        final_image[:,(64*i):(64*(i+1)),:] = temporary[i]

    pixel_count = {}
    pixel_count['c0']=c0
    pixel_count['c1']=c1
    pixel_count['c2']=c2
    pixel_count['c3']=c3
    pixel_count['c4']=c4
    pixel_count['c5']=c5
    pixel_count['c6']=c6
    pixel_count['c7']=c7
    imsave(results_path+name,final_image)
    results = {'final_image':final_image,'pixel_count':pixel_count}
    return results

