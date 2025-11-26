import tensorflow as tf
import matplotlib.pyplot as ptl
import pandas as pd
import seaborn as sns

## data preprocessing

# Google Drive folder ID
ZIP_NAME = "Plant_Dataset.zip"

# Download folder as zip
if not os.path.exists("data"):
    print("Downloading dataset from Google Drive...")
    gdown.download_folder(
        "https://drive.google.com/drive/folders/1EtSGVi8TMPbX4DDQUCl_xdY_iRjSmZxQ?usp=drive_link",
        output=ZIP_NAME,
        quiet=False,
        use_cookies=True
    )

    # Extract the downloaded ZIP
    print("Extracting dataset...")
    with zipfile.ZipFile(ZIP_NAME, "r") as zip_ref:
        zip_ref.extractall("data/")

## Training Image PreProcessing

train_int = "data/Plant Dataset/Train"
test_int = "data/Plant Dataset/Test"
validation_int = "data/Plant Dataset/Validation"


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

# Exporting datasets and constants so CNN_Build.py can use them.
__all__ = ["train_ds", "val_ds", "test_ds", "IMG_SIZE", "class_names"]
