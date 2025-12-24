import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D,MaxPool2D,Flatten,Dense,Dropout

DATA_PATH = r"C:\Projects\Thamizhan_Skills\Project3\data"
IMG_HEIGHT = 30
IMG_WIDTH = 30
CATEGORY = 3
CHANNEL = 3
print("Initializing basic parameters and starting to open file")

images =[]
labels =[]

for root,dirs,files in os.walk(DATA_PATH):
    for i in dirs:
        path = os.path.join(DATA_PATH,i)
        for img in os.listdir(path):
            try:
                imag = cv2.imread(os.path.join(path,img))
                imag = cv2.resize(imag, (30,30))
                images.append(imag)
                labels.append(i)
            except Exception as e:
                print(f"Error Occured {e}")
X = np.array(images)
Y = np.array(labels)
print("generated x,y np array and proceeding to normalising and one hot encoding")
X = X/255.0
Y = to_categorical(Y,CATEGORY)

x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size =0.2, random_state = 42)
print("splited the test and train data to train the dta and to test it and proceeding to crating the nn layer")
model = Sequential([
    Conv2D(filters = 32, kernel_size = (3,3), activation ="relu", input_shape = (IMG_HEIGHT,IMG_WIDTH,CATEGORY)),
    MaxPool2D((2,2)),
    Dropout(0.25),

    Conv2D(64,(3,3),activation = 'relu'),
    MaxPool2D((2,2)),
    Dropout(0.25),

    Flatten(),
    Dense(128,activation = 'relu'),
    Dense(CATEGORY,activation = 'softmax')
    ])
model.compile(optimizer = 'adam',loss = 'categorical_crossentropy',metrics = ['accuracy'])
model.summary()
print("Starting fix7&learning")
model.fit(x_train,y_train,epochs = 15, validation_data = (x_test,y_test),verbose =2)

model.save('traffic_signal1.h5')
print('Saved Sucessfully')
