# Serve model as a flask application

import os
import json
from unittest import result
import numpy as np
import tensorflow as tf
from skimage.color import rgb2lab, lab2rgb
from flask import Flask, request, Response
from tensorflow.keras.preprocessing.image import img_to_array, load_img

model = None
app = Flask(__name__)
model_path = "../model_final/0402_3kimg_8-e04"

def load_model():
    global model
    the_model = tf.keras.models.load_model("model_final/0402_3kimg_8-e04")


@app.route('/')
def home_endpoint():
    return 'Hello World!'


@app.route('/predict', methods=['POST'])

# def image_inputProcess():
#     imgs = []
#     imgs.append(img_to_array(load_img("./usrInput/user" + str(order)  + ".jpg", target_size=(256, 256))))

# def get_prediction():
#     # Works only for a single sample
#     if request.method == 'POST':
#         data = request.get_json()  # Get data posted as a json
#         data = np.array(data)[np.newaxis, :]  # converts shape from (4,) to (1, 4)
#         prediction = model.predict(data)  # runs globally loaded model on the data
#     return str(prediction[0])




# 定义接口地址为imageprocess
@app.route('/imageprocess', methods=['POST'])
def image_preprocess():
	# 获取到post请求传来的file里的image文件
    image = request.files.get("image")

    # 获取到post请求里传来的form表单中的文件名字段
    imageName = request.form.get("filename")

    print(imageName)
    print(image)

    if image is None:
        return "nothing found"

    # 获取到的文件名，将文件存放到对应的位置
    image.save("./UserUpload/"+ str(imageName) +".jpeg")
    return "图片上传成功"


@app.route('/predict', methods=['POST'])
#     # Works only for a single sample
def get_prediction():
    imageName = request.form.get("filename") 
    imgs = []
    imgs.append(img_to_array(load_img("./UserUpload/"+ str(imageName) +".jpeg", target_size=(256, 256))))
    
    # reshape
    imgs = np.array(imgs, dtype=float) / 255.0
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

    y_pred_rgb = [lab2rgb(lab) for lab in y_pred_lab[0, :, :, :]]
    
    # Save image to Output dir
    
    
    return  


@app.route("/output/<imageName>.jpeg")
def get_frame(imageName):
    # 去对应的文件夹找到对应名字的图片
    with open(r'/output/{}.jpeg'.format(imageName), 'rb') as f: 	
        image = f.read()
        # 返回给用户
        result = Response(image, mimetype="image/jpeg")
        return result



if __name__ == '__main__':
    load_model()  # load model at the beginning once only
    app.run(host='0.0.0.0', port=80)