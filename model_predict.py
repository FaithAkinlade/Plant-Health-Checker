# Project: Plant Health Checker
# Students: Faith Akinlade, Smit Desai, Pratham Waghela (Group 7)
# Description: Loads the trained CNN model and class names, and provides a function to predict the health status of a
# plant from a given image. Returns the predicted class and confidence score.

# model_predict.py
import tensorflow as tf
import numpy as np
import json

# Loading model
model = tf.keras.models.load_model("plant_health_model.keras")

# Loading class names
with open("class_names.json", "r") as f:
    class_names = json.load(f)

IMG_SIZE = (224, 224)

def predict_image(image_path):
    """
    This function uses the model build in CNN_Build.py to predict the status of the plant's health based on the
    available data.
    :param: image_path: path of image uploaded by user
    :return: name of plant health class, confidence in prediction
    """
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=IMG_SIZE)
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    class_index = np.argmax(prediction)
    confidence = float(np.max(prediction)) * 100

    return class_names[class_index], confidence
