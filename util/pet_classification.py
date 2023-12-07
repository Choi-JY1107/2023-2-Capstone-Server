import numpy as np
from keras.models import load_model


def predict_pet(image):
    model_path = 'keras_model/pet_classification_efficientnet.h5'
    class_path = 'keras_model/class_list.txt'
    rank_list = []

    # model, class_list 불러오기
    model = load_model(model_path)
    _file = open(class_path, 'r')
    file = _file.readlines()
    label_list = [x.strip() for x in file]
    _file.close()

    # 이미지 데이터 표준화
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    target_image = image.resize((224, 224))
    image_array = np.asarray(target_image)
    normalized_image_array = image_array / 255.0
    data[0] = normalized_image_array

    # Make the prediction
    prediction = model.predict(data)
    arr = prediction[0].tolist()
    for index, value in enumerate(arr):
        rank_list.append((label_list[index], value))
    rank_list.sort(key=lambda x: -x[1])

    print(rank_list)
    return rank_list
