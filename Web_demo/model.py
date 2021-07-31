#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys 
from flask import Flask , render_template, request
import pickle
import numpy as np
import re
import json
import os , sys


#khởi tạo flask
app = Flask(__name__)


# Cấu hình thư mục sẽ upload file lên
app.config["UPLOAD_FOLDER"] = "static"


# load lại model
file = open("model.sav","rb")
model = pickle.load(file)
vectorizer_file = open("vectorizer.sav", "rb")
vectorizer = pickle.load(vectorizer_file)


#tiền xử lý dữ liệu
def processing(text, word_segment , lower_case):  
  #remove các ký tự kéo dài
    text = re.sub(r'([A-Za-zaăâbcdđeêghiklmnoôơpqrstuưvxyàằầbcdđèềghìklmnòồờpqrstùừvxỳáắấbcdđéếghíklmnóốớpqrstúứvxýảẳẩbcdđẻểghỉklmnỏổởpqrstủửvxỷạặậbcdđẹệghịklmnọộợpqrstụựvxỵãẵẫbcdđẽễghĩklmnõỗỡpqrstũữvxỹAĂÂBCDĐEÊGHIKLMNOÔƠPQRSTUƯVXYÀẰẦBCDĐÈỀGHÌKLMNÒỒỜPQRSTÙỪVXỲÁẮẤBCDĐÉẾGHÍKLMNÓỐỚPQRSTÚỨVXÝẠẶẬBCDĐẸỆGHỊKLMNỌỘỢPQRSTỤỰVXỴẢẲẨBCDĐẺỂGHỈKLMNỎỔỞPQRSTỦỬVXỶÃẴẪBCDĐẼỄGHĨKLMNÕỖỠPQRSTŨỮVXỸ])\1+', lambda m: m.group(1), text)
    # #Remove sign
    sign = r"[!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~\'\'""''``]"
    text =re.sub(sign, " ", text)
   #Chuyển thành chữ thường
    if lower_case == True:
        text = text.lower()
    if word_segment == True:
        text = re.sub("\\s+", " ", text)
  #chuẩn hóa các từ không
    replace_list = json.load(open("replace_list.txt"))
    for k, v in replace_list.items():
        text = text.replace(k, v)
    # if word_segment == True:
    #     #segments = rdrsegmenter.tokenize(text)
    #     text = " ".join(segments[0])
    return text
  # loại bỏ stopword:

def return_result(str):
    str = processing(str, True, True)
    vector  = vectorizer.transform([str])
    predict = model.predict(vector)
    if (predict[0] == 1):
        return "Positive"
    elif (predict[0] == 0):
        return "negative"
    else:
        return "Neutral"


# Xử lý request
@app.route("/", methods = ["POST", "GET"])
def HOME():
    if request.method == "GET":
        return render_template("index.html")
    else:
        text = request.form['text']
        mess = return_result(text)
        return render_template("index.html", msg = mess)
    return "ĐÂy là home"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 9999 , debug= True)
    



