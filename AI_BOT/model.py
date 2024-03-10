from keras.models import load_model  
from PIL import Image, ImageOps  
import numpy as np


def get_class(image, model, labels):
    try:
        np.set_printoptions(suppress=True)
        model = load_model(model, compile=False)
        class_names = open(labels, "r", encoding='utf-8').readlines()

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        image = Image.open(image).convert("RGB")

        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

        image_array = np.asarray(image)

        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        data[0] = normalized_image_array

        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        harmful_food_index = 0
        healthy_food_index = 1

        if prediction[0][harmful_food_index] > prediction[0][healthy_food_index]:
            advice = "Мы рекомендуем сбалансировать ваш ужин и сделать его более полезным."
        else:
            advice = "Мы рекомендуем сделать ваш ужин более сбалансированным"

        return class_name[2:-1], confidence_score, advice
    except Exception as e:
        return "Не удалось распознать изображение", 0.0, "Пожалуйста, прикрепите правильное изображение"


