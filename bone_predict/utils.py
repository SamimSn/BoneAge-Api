from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.xception import (
    preprocess_input,
)
import numpy as np
from keras.metrics import mean_absolute_error
from ultralytics import YOLO
import threading

# Define lock for thread safety when using shared resources
lock = threading.Lock()

# Load the model globally, outside of the function to avoid reloading in each thread
bone_model = load_model(
    "V1.h5", custom_objects={"mae_in_months": mean_absolute_error}
)

is_valid_model = YOLO("Obj.pt")


def predict_is_image_valid(img):
    with lock:
        results = is_valid_model(img)
        probs = results[0].probs
        prob_values = probs.data
        hand_prob = prob_values[0].item()
        if hand_prob > 0.5:
            return True
        else:
            return False


def mae_in_months(x_p, y_p):
    """function to return mae in months"""
    return mean_absolute_error(
        (41.182021399396326 * x_p + 127.3207517246848),
        (41.182021399396326 * y_p + 127.3207517246848),
    )


def predict_bone_age(path):
    with lock:
        image = Image.open(path)

        if image.mode != "RGB":
            image = image.convert("RGB")

        target_size = (256, 256)
        image = image.resize(target_size)

        img_array = img_to_array(image)

        img_array = preprocess_input(img_array)

        img_array = np.expand_dims(img_array, axis=0)

        # Predict using the loaded model
        pred = 127.3207517246848 + 41.182021399396326 * bone_model.predict(
            img_array
        )

        print(f"Predicted bone age: {pred}")

    return pred[0][0]


def predict_bone_age_in_thread(path):
    """Wrapper function to be executed in a thread"""
    try:
        return predict_bone_age(path)
    except Exception as e:
        print(f"Error during prediction for {path}: {e}")


def predict_is_image_valid_in_thread(path):
    """Wrapper function to be executed in a thread"""
    try:
        return predict_is_image_valid(path)
    except Exception as e:
        print(f"Error during prediction for {path}: {e}")
