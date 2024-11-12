import tensorflow as tf
import numpy as np
from PIL import Image
from datetime import datetime
from backend.config.db_conn import insert

# TFLite 모델 경로
model_path = 'backend/models/classification_mobilenet_v3_small_best.tflite'

# 모델 클래스 값
CIFAR100_CLASSES = ['apple', 'aquarium_fish', 'baby', 'bear', 'beaver', 'bed', 'bee', 'beetle', 'bicycle', 'bottle', 'bowl', 'boy', 'bridge', 'bus', 'butterfly', 'camel', 'can', 'castle', 'caterpillar', 'cattle', 'chair', 'chimpanzee', 'clock', 'cloud', 'cockroach', 'couch', 'crab', 'crocodile', 'cup', 'dinosaur', 'dolphin', 'elephant', 'flatfish', 'forest', 'fox', 'girl', 'hamster', 'house', 'kangaroo', 'keyboard', 'lamp', 'lawn_mower', 'leopard', 'lion', 'lizard', 'lobster', 'man', 'maple_tree', 'motorcycle', 'mountain', 'mouse', 'mushroom', 'oak_tree', 'orange', 'orchid', 'otter', 'palm_tree', 'pear', 'pickup_truck', 'pine_tree', 'plain', 'plate', 'poppy', 'porcupine', 'possum', 'rabbit', 'raccoon', 'ray', 'road', 'rocket', 'rose', 'sea', 'seal', 'shark', 'shrew', 'skunk', 'skyscraper', 'snail', 'snake', 'spider', 'squirrel', 'streetcar', 'sunflower', 'sweet_pepper', 'table', 'tank', 'telephone', 'television', 'tiger', 'tractor', 'train', 'trout', 'tulip', 'turtle', 'wardrobe', 'whale', 'willow_tree', 'wolf', 'woman', 'worm']

def tflite_predict_image(request_id: str, image_path: str, start_time: datetime, temperature=1.0):
    # TFLite 모델 로드
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

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
    img_array = np.expand_dims(img_array, axis=0)  # 배치 차원 추가 (1, 128, 128, 3)

    # TFLite 모델에 입력 설정
    input_details = interpreter.get_input_details()
    print(f"Input shape: {input_details[0]['shape']}")  # 입력 차원 출력
    interpreter.set_tensor(input_details[0]['index'], img_array)

    # 출력 세부 정보 가져오기
    output_details = interpreter.get_output_details()
    print(f"Output shape: {output_details[0]['shape']}")  # 출력 차원 출력

    # 추론 실행
    interpreter.invoke()

    # 출력값 가져오기
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # 로짓값에 Softmax 적용
    probabilities = softmax(output_data[0], temperature)

    # 예측된 클래스
    predicted_class = CIFAR100_CLASSES[np.argmax(probabilities)]

    # 런타임 종료 시간
    runtime = datetime.now() - start_time
    runtime_seconds = runtime.total_seconds()

    # 결과 저장 (DB 저장 로직)
    insert(request_id, image_path, predicted_class, runtime_seconds)

    return predicted_class

# Softmax 함수
def softmax(x, temperature=1.0):
    e_x = np.exp((x - np.max(x)) / temperature)
    return e_x / e_x.sum(axis=-1, keepdims=True)
