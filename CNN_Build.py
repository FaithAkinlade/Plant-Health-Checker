from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import Preprocess_Data as data   # FIXED import

# Getting the variables from PreProcess_Data.py
train_ds = data.train_ds
val_ds = data.val_ds
IMG_SIZE = data.IMG_SIZE
num_classes = len(data.class_names)