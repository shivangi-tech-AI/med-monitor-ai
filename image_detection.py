import cv2
import tensorflow as tf
import numpy as np

# Load the trained CNN model
model = tf.keras.models.load_model('models/pill_cnn_model.h5')

def detect_pill(path):
    image = tf.keras.preprocessing.image.load_img(path, target_size=(64, 64))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0) / 255.0

    prediction = model.predict(image)
    print("Prediction score:", prediction)

    if prediction[0][0] > 0.5:
        return "Pill Detected"
    else:
        return "No Pill"

# Run this script directly to test
if __name__ == "__main__":
    result = detect_pill()
    print("🔍 Result:", result)
