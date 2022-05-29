
# Importing flask module in the project is mandatory



import re
import PIL
import base64
import numpy as np
import tensorflow as tf


from io import BytesIO
from flask_cors import CORS
import os
from flask import Flask, request, render_template, send_from_directory
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb



app = Flask(__name__, static_folder='static/build/')
cors = CORS(app)


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.



@app.route('/process', methods=['POST'])
def process():
    # data:image/png;base64,
    img = tf.io.decode_base64(re.sub("\\+", "-", re.sub("/", "_", request.form.get("base64", "")[22:])))
    img = tf.image.decode_image(img, channels=3)

    # reshape
    imgs = np.array([img_to_array(img)], dtype=float) / 255.0
    labs = np.array([rgb2lab(rgb) for rgb in imgs])

    x_test = labs[:, :, :, 0]
    x_test = x_test.reshape(x_test.shape + (1, ))

    # predict
    y_pred = model.predict(x_test)


    # prediction reshape
    y_pred_ab = y_pred * 128.0
    y_pred_lab = np.zeros(labs.shape)

    y_pred_lab[0, :, :, 0] = x_test[0].reshape(x_test.shape[1:3])
    y_pred_lab[0, :, :, 1:] = y_pred_ab[0]

    y_pred_rgb = np.array([lab2rgb(lab) * 255 for lab in y_pred_lab[0, :, :, :]], dtype=np.uint8)
    # print(y_pred_rgb, base64.urlsafe_b64encode(y_pred_rgb)[:50])

    img = PIL.Image.fromarray(y_pred_rgb).convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    img_byte = buffered.getvalue()
    img_str = "data:image/png;base64," + base64.b64encode(img_byte).decode()

    # return base64.urlsafe_b64encode(y_pred_rgb)
    # print(img_str[:50])
    return img_str

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# @app.route("/")
# def render():
#     return render_template('index.html')

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    model = tf.keras.models.load_model("./0402_3kimg_8-e04")
    app.run(host='0.0.0.0', port=5000)

