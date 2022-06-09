from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
from tensorflow import keras
import tensorflow as tf
import io
import os
from db import get, get_one, create
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


model = keras.models.load_model("model.h5")


def transform_image(pillow_image):
    data = np.asarray(pillow_image)
    data = data / 255.0
    data = tf.image.resize(data, [400, 400])
    data = np.expand_dims(data, 0)
    return data


def predict(x):
    predictions = model(x)
    predictions = tf.nn.softmax(predictions)
    pred0 = predictions[0]
    label0 = np.argmax(pred0)
    return label0


app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return "OK"

@app.route("/predict", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            image_bytes = file.read()
            pillow_img = Image.open(io.BytesIO(
                image_bytes))
            tensor = transform_image(pillow_img)
            prediction = predict(tensor)
            fish = get_one(prediction)
            data = {"prediction": fish}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=False)
