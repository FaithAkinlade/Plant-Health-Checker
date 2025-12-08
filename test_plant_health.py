# Author: Faith Akinlade (Group 7)
# Date: 11/25/2025
# Description: Testing file for various parts of the plant health Checker program.

import os
import pytest
import tensorflow as tf
import numpy as np
from PIL import Image
from image_preprocessing_file import train_ds, val_ds, test_ds, class_names, IMG_SIZE
from model_predict import predict_image, model  # Replace with actual filename if needed


# 1. Test that datasets are loaded and non-empty
def test_datasets_not_empty():
    assert train_ds is not None
    assert val_ds is not None
    assert test_ds is not None

    train_batches = list(train_ds.take(1))
    val_batches = list(val_ds.take(1))
    test_batches = list(test_ds.take(1))
    assert len(train_batches) > 0
    assert len(val_batches) > 0
    assert len(test_batches) > 0

# 2. Test that class names are loaded
def test_class_names():
    assert isinstance(class_names, list)
    assert len(class_names) > 0
    for cls in class_names:
        assert isinstance(cls, str)

# 3. Test model is loaded
def test_model_loaded():
    assert model is not None
    # Check model has input layer compatible with IMG_SIZE
    input_shape = model.input_shape
    assert input_shape[1:3] == IMG_SIZE

# 4. Test predict_image function with a dummy image
def test_predict_image(tmp_path):
    # Create a dummy RGB image
    img_path = tmp_path / "test_image.jpg"
    dummy_image = Image.fromarray(np.uint8(np.random.rand(224,224,3)*255))
    dummy_image.save(img_path)

    # Running prediction
    predicted_class, confidence = predict_image(str(img_path))

    # Test outputs
    assert predicted_class in class_names
    assert isinstance(confidence, float)
    assert 0 <= confidence <= 100

# 5. Test normalization to ensure that the dataset images are scaled correctly between 0 and 1, and that the labels are
# categorical
def test_train_ds_normalization():
    batch_images, batch_labels = next(iter(train_ds))
    # All pixel values should be between 0 and 1 after normalization
    assert tf.reduce_max(batch_images) <= 1.0
    assert tf.reduce_min(batch_images) >= 0.0
    # Labels should sum to 1 (categorical)
    assert tf.reduce_all(tf.reduce_sum(batch_labels, axis=1) == 1)
