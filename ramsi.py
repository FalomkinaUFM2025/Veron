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
def put_russian_text(img, text, position, font_scale, color, thickness):
    #пробуем разные шрифтики :3
    fonts = [
        cv2.FONT_HERSHEY_COMPLEX,
        cv2.FONT_HERSHEY_COMPLEX_SMALL,
        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    ]

    #создаем временное изображение для тэкста
    text_img = np.zeros_like(img)

    for font in fonts:
        try:
            cv2.putText(text_img, text, position, font, font_scale, color, thickness)
            #если текст отрисовался не пустой, то сбегаем из цыкла за пирожками
            if np.max(text_img) > 0:
                break
        except:
            continue

    #если нифига не вышло используем инглиш вери вери гуд аналаги
    if np.max(text_img) == 0:
        trans_table = str.maketrans(
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
            "abBrdeex3unKnmHonpcTyoxu4wwib9io0aABBrDEEX3UNKNMHONPCTYOXU4WWIB9IO0A"
        )
        text = text.translate(trans_table)
        cv2.putText(text_img, text, position,  cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

    #наклвадываем текст на исходное изоброжение
    img = cv2.addWeighted(img, 1, text_img, 1, 0)
    return img


print("для закрытия нажмите й в окне с изображением")

# для повышения производительности обрабатываем каждый ный кадр
frame_counter = 0
skip_frames = 1 # кажды второй кадр обрабатываем в формалине
emotion_result = None

while True:
    ret, frame = cap.read()
    if not ret:
        print('ошибка не удалос получит кадр')
        break

    frame_counter += 1

    # конвертируем в оттенки серого цвета для распознования лиц
    gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #ДЕТЕКЦИЯ ЛИЦ НА КАРТИНКЕ
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize = (30,30)
    )

    # находим все хари на экране и обрабатываем кислотой (;3)
    for (x, y, w, h) in faces:
        # рисуем основной прямоугольник
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 2)

        # рисуем дополнительные елементы для style
        corner_lenght = min(w, h) // 4
        # левый верхний шизоид
        cv2.line(frame, (x, y), (x + corner_lenght, y), (0, 255, 255), 2)
        cv2.line(frame, (x, y), (x, y + corner_lenght), (0, 255, 255), 2)
        # правый верхний шизоид
        cv2.line(frame, (x + w, y), (x + w - corner_lenght, y), (0, 255, 255), 2)
        cv2.line(frame, (x + w, y), (x + w + corner_lenght, y), (0, 255, 255), 2)
        # левый нижний шизоид
        cv2.line(frame, (x, y + h), (x + corner_lenght, y + h), (0, 255, 255), 2)
        cv2.line(frame, (x + w, y + h), (x + w, y + h - corner_lenght), (0, 255, 255), 2)

        # распознаем эмоции в каждом N-ном кадрэ
        if frame_counter % skip_frames == 0:
            try:
                # подготавлием личико к распознаванию эмоций(тушь ресничке помадка)
                face_roi = frame[y:y + h, x:x + w]

                # начищаем морду для модели ксенова
                face_roi = cv2.resize(face_roi, (224,224)) # размер картнки ожидаемой модели
                face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB) # модель ажидает rgb

                #нормолизация
                face_roi = face_roi.astype(np.float32) / 255.0

                # ПРЕОБРАЗУЕМ В ФОРМАТ [1,3,224,224]\
                input_data = np.expand_dims(face_roi.transpose(2, 0, 1), axis=0)

                # онкс рантайм распознает эиоцию
                outputs = session.run(None, {input_name: input_data})
                emotions = outputs[0][0]

                #определяем домининирующую эмоцию
                emotion_index = np.argmax(emotions)
                emotion_keys = list(emotion_labels.keys())
                emotion_key = emotion_keys[emotion_index]
                emotion = emotion_labels[emotion_key]
                confidence = emotions[emotion_index]

                # сохраняем результат для его отображения
                emotion_result = (emotion, confidence)
            except Exception as e:
                print(f'error of emotion recognition: {e}')
                emotion_result = ('error', 0.0)

                # отображаем эмоции рядом с рамкой
        elif emotion_result:
            emotion, confidence = emotion_result
            emotion_text = f'{emotion}({confidence:.2f})'

            #  позиция текста  справа от рамки
            text_x = x + w + 10
            text_y = y + h // 2

            # проверка чтоб текст не выходил за рамки кадра
            text_width = 200 # примерная ширина текста
            if text_x + text_width > frame.shape[1]:
                text_x = x - text_width - 10
            # рисуем фон для текста
            cv2.rectangle(frame,
                          (text_x - 5, text_y - 25),
                          (text_x + text_width, text_y + 10),
                          (0,0,0), - 1)

            # выводим текст с эмоцией
            frame = put_russian_text(frame, emotion_text, (text_x, text_y), 0.7, (0, 255, 255), 2)

            #отображаем кол-во лиц
            count_text = f"лиц: {len(faces)}"
            cv2.rectangle(frame, (5, 5), (150,40), (0, 0, 0), -1)
            frame = put_russian_text(frame, count_text, (10, 30), 0.7, (0, 0, 255), 2)

            # отоьражаем фпс
            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps <= 0:
                if "last_time" not in globals():
                    last_time = cv2.getTickCount()
                current_time = cv2.getTickCount()
                elapsed_time = (current_time - last_time) / cv2.getTickFrequency()
                if elapsed_time > 0:
                    fps = 1.0 / elapsed_time
                last_time = current_time
            fps_text = f"FPS: {int(fps)}"
            cv2.rectangle(frame, (frame.shape[1] - 150, 5), (frame.shape[1] - 5, 40), (0, 0, 0), -1)
            frame = put_russian_text(frame, fps_text, (frame.shape[1] - 140, 30), 0.7, (0, 255, 255), 2)

            # отображаем кадр
            cv2.imshow("распознавание лиц и эмоций", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()
