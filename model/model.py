
from sklearn.datasets import load_files
from keras import applications
from keras.utils import np_utils
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.models import Model
from keras.preprocessing import image
from tqdm import tqdm
import numpy as np
from glob import glob
import h5py 

def build_model(num_classes):
	# Use VGG16 model trained on Image Net and finetune the top layer
	vgg16_model = applications.VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
	print('Model loaded')
	for layer in vgg16_model.layers:
		#Freeze imagenet trained layers
		layer.trainable = False

	top_model = Flatten()(vgg16_model.output)
	top_model = Dense(256, activation='relu')(top_model)
	top_model = Dropout(0.5)(top_model)
	top_model = Dense(num_classes, activation='sigmoid')(top_model)

	# Build a model made up of top_model stuck to the end of vgg16_model
	model = Model(vgg16_model.input, top_model)

	# Print the content/size of layers
	model.summary()
	return model

if __name__ == '__main__':
	build_model()

