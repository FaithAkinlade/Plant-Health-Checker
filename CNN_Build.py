from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import Preprocess_Data as data 

# Getting the variables from PreProcess_Data.py
train_ds = data.train_ds
val_ds = data.val_ds
IMG_SIZE = data.IMG_SIZE
num_classes = len(data.class_names)

# Initializing the model
model = Sequential([
    # Adding convolutional layers (these layers learn features by applying filters to small regions of the image.
    Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
    # These layers downsample the feature maps, reducing dimensionality and computational cost while retaining 
    # important features.
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    # Converting 2D feature map into a 1D vector before connecting to fully connected layers.
    Flatten(),
    # Dense layers learn to classify the extracted features.
    Dense(128, activation='relu'),
    Dropout(0.4),
    Dense(num_classes, activation='softmax')  # Use correct num_classes
])

# Compiling the model
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Training the model
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10
)
