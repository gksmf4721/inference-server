import onnxruntime as ort
import os
from PIL import Image
import numpy as np

# Softmax 함수
def softmax(x, temperature=1.0):
    e_x = np.exp((x - np.max(x)) / temperature)
    return e_x / e_x.sum(axis=-1, keepdims=True)

# ONNX 모델 로드
model_path = 'backend/models/classification_mobilenet_v3_small_best.onnx'
session = ort.InferenceSession(model_path)

# 모델 클래스 값
CIFAR100_CLASSES = ['apple', 'aquarium_fish', 'baby', 'bear', 'beaver', 'bed', 'bee', 'beetle', 'bicycle', 'bottle', 'bowl', 'boy', 'bridge', 'bus', 'butterfly', 'camel', 'can', 'castle', 'caterpillar', 'cattle', 'chair', 'chimpanzee', 'clock', 'cloud', 'cockroach', 'couch', 'crab', 'crocodile', 'cup', 'dinosaur', 'dolphin', 'elephant', 'flatfish', 'forest', 'fox', 'girl', 'hamster', 'house', 'kangaroo', 'keyboard', 'lamp', 'lawn_mower', 'leopard', 'lion', 'lizard', 'lobster', 'man', 'maple_tree', 'motorcycle', 'mountain', 'mouse', 'mushroom', 'oak_tree', 'orange', 'orchid', 'otter', 'palm_tree', 'pear', 'pickup_truck', 'pine_tree', 'plain', 'plate', 'poppy', 'porcupine', 'possum', 'rabbit', 'raccoon', 'ray', 'road', 'rocket', 'rose', 'sea', 'seal', 'shark', 'shrew', 'skunk', 'skyscraper', 'snail', 'snake', 'spider', 'squirrel', 'streetcar', 'sunflower', 'sweet_pepper', 'table', 'tank', 'telephone', 'television', 'tiger', 'tractor', 'train', 'trout', 'tulip', 'turtle', 'wardrobe', 'whale', 'willow_tree', 'wolf', 'woman', 'worm']


def predict_image(image_path: str, temperature=1.0):
    # 이미지 로드
    img = Image.open(image_path)

    # 이미지 크기 변경 및 정규화
    img = img.resize((128, 128))  # 모델에 맞게 리사이즈
    img_array = np.array(img).astype(np.float32)  # 이미지를 NumPy 배열로 변환

    # 정규화
    img_array /= 255.0  # [0, 1] 범위로 정규화

    # 이미지가 그레이스케일인 경우 처리
    if len(img_array.shape) == 2:  # (height, width)
        img_array = np.expand_dims(img_array, axis=-1)

    # 모델 입력 형식에 맞게 이미지 형태 변환
    img_array = np.transpose(img_array, (2, 0, 1))
    img_array = np.expand_dims(img_array, axis=0)

    # 추론 실행
    inputs = {session.get_inputs()[0].name: img_array}
    outputs = session.run(None, inputs)

    # 로짓값에 Softmax 적용
    logits = outputs[0]
    probabilities = softmax(logits, temperature)

    # 예측된 클래스
    predicted_class = np.argmax(probabilities)

    return CIFAR100_CLASSES[predicted_class]

