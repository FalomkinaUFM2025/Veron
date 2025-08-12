from ipaddress import summarize_address_range

import cv2
import numpy as np
from urllib.request import urlretrieve
import os
import onnxruntime as ort #используем онкс вместо опен св

# фигачим модель ксенова шоб работало
model_url = "https://huggingface.co/Xenova/facial_emotions_image_detection/resolve/main/onnx/model.onnx"
model_path = "model.onnx"

if not os.path.exists(model_path):
    print("Загрузка модели распознаваний эмотионс ксинова")
    urlretrieve(model_url, model_path)
    print("Модель загружена, урааааа :D")

#Загружаем классификатор для распознавания морд :D
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascades_frontalface_default.xml'
)

#Инициализируем онкс рантайм инит
session = ort.InferenceSession(model_path)
input_name = session.get_inputs()[0].name

#создаем объект для захвата видево
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("мяу, загружаеца :3")
    exit()

#названия эмоций
emotion_labels = {
    "angry": "Злость",
    "disgust": "Отвращение",
    "fear": "Страх",
    "happy": "Счастье",
    "sad": "Грусть",
    "surprise": "Удивление",
    "neutral": "Нейтрально"
}
#функция для отображения русского текста
def put_russian_text(img, text, position, pont_scale, color, thickness):
    #пробуем разные шрифтики :3
    fonts = [
        cv2.FONT_HERSHEY_COMPLEX,
        cv2.FONT_HERSHEY_COMPLEX_SMALL,
        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    ]

    #создаем временное изображение для тэкста
# дз создать презентацию нашему проекту

