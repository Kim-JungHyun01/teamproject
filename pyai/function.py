import io
import base64
import numpy as np

from pydantic import BaseModel
from PIL import Image, ImageDraw
from model import load_model

import logging
logging.basicConfig(level=logging.INFO)

# 메시지출력 및 이미지 출력함수
class DetectionResult(BaseModel):
    message : str
    image : str

# 알파채널(A_필터)이 있다면 제거하고 RGB로 변환
def removal_filter(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image

# 예측(이미지 객체 이용)
def model_predict(image, confidence, overlap):
    model = load_model()
    img = np.array(image)  # 이미지 numpy 배열 반환
    result_image = model.predict(img, confidence=confidence, overlap=overlap).json()
    return result_image

#바운딩박스
def draw_bounding_box(image: Image, result):
    draw=ImageDraw.Draw(image)
    for pred in result['predictions']:
        # 예측된 박스의 xy 중점
        x = pred['x']
        y = pred['y']
        width = pred['width']
        height = pred['height']
        x1 = int(x - width/2)
        y1 = int(y - height/2)
        x2 = int(x + width/2)
        y2 = int(y + height/2)
        class_name = pred['class']
        confidence = pred['confidence']
        #바운딩박스
        draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=3)
        # 글자박스
        draw.rectangle([(x1, y1-20), (x1+width, y1)], fill="white")
        draw.text((x1, y1-15), f'{class_name} {confidence : .2f}', fill="black", size=30)
    return image

# 이미지 결과를 base64로 인코딩
def encode_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format='JPEG')  # JPEG로 이미지저장
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str