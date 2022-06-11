import os

from db import get_one
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import io
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image

from flask import Flask, request, jsonify

model = keras.models.load_model("model.h5")


def transform_image(pillow_image):
    data = np.asarray(pillow_image)
    data = data / 255.0
    data = tf.image.resize(data, [400, 400])
    _,_,chanel = data.shape
    if chanel > 3:
        data = data[:,:,:3] # Incase jika imagenya lebih dari 3 channel
    data = np.expand_dims(data,0) 
    return data


def predict(x):
    predictions = model(x)
    predictions = tf.nn.softmax(predictions)
    pred0 = predictions[0].numpy()
    labels = np.argsort(pred0)[-3:]
    result = []
    for label in range(2,-1,-1):
        idx = labels[label]
        result.append((idx,pred0[idx]))
    #label0 = np.argmax(pred0)
    #prob0 = pred0[label0].numpy()
    return result #(label0,prob0)

app = Flask(__name__)

@app.route("/predict", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            image_bytes = file.read()
            pillow_img = Image.open(io.BytesIO(image_bytes)) #Diapus convert('L')
            tensor = transform_image(pillow_img)
            prediction = predict(tensor)
            fish = get_one(prediction)
            data = {"prediction": fish}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"


if __name__ == "__main__":
    app.run(debug=False)