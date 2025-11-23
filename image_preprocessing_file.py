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
