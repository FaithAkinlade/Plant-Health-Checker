import tensorflow as tf
import matplotlib.pyplot as ptl
import pandas as pd
import seaborn as sns

## data preprocessing
## Training Image PreProcessing

train_int = "/kaggle/input/plant-health-checker/Plant Dataset/Train"
test_int = "/kaggle/input/plant-health-checker/Plant Dataset/Test"
validation_int = "/kaggle/input/plant-health-checker/Plant Dataset/Validation"

IMG_SIZE = (224,224)
BATCH_SIZE = 32

train_dir = tf.keras.preprocessing.image_dataset_from_directory(
    train_int,
    image_size = IMG_SIZE,
    batch_size = BATCH_SIZE,
    label_mode = "categorical"
    
)

test_dir = tf.keras.preprocessing.image_dataset_from_directory(
    test_int,
    image_size = IMG_SIZE,
    batch_size = BATCH_SIZE,
    label_mode = "categorical"
    
)

validation_dir = tf.keras.preprocessing.image_dataset_from_directory(
    validation_int,
    image_size = IMG_SIZE,
    batch_size = BATCH_SIZE,
    label_mode = "categorical"
    
)

## Normalizing the image to the Pixel size (0-255 -> 0-1)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_dir.map(lambda x, y: (x/255.0, y)).cache().prefetch(AUTOTUNE)
val_ds = validation_dir.map(lambda x, y: (x/255.0, y)).cache().prefetch(AUTOTUNE)
test_ds = test_dir.map(lambda x, y: (x/255.0, y)).cache().prefetch(AUTOTUNE)

class_names = train_dir.class_names
print("Classes:", class_names)

