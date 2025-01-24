import io

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel

import base64
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 로깅 설정
import logging
logging.basicConfig(level=logging.INFO)

#roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="tL1AfLNsLR2QJIERYzOp")
project = rf.workspace("teamproject-a4e2e").project("teem3")
version = project.version(4)
# dataset = version.download("yolov11")
model = version.model

app = FastAPI()

# 메시지출력 및 이미지 출력함수
class DetectionResult(BaseModel):   # pydantic을 사용하여 데이터 모델을 정의 (응답 데이터를 구조화)
    message : str                   # 클라이언트가 보낸 메세지
    image : str                     # base64로 인코딩된 탐지 결과 이미지

# 바운딩 박스
def draw_bounding_box(image : Image, result_image):
    # 바운딩 박스 그리기
    draw = ImageDraw.Draw(image)
    for prediction in result_image['predictions']:
        x = prediction['x']
        y = prediction['y']
        width = prediction['width']
        height = prediction['height']
        x1 = int(x - width / 2)
        y1 = int(y - height / 2)
        x2 = int(x + width / 2)
        y2 = int(y + height / 2)
        logging.info(f"바운딩 박스 좌표 : {x1} {y1} {x2} {y2}")
        class_name = prediction['class']
        confidence = prediction['confidence']
        logging.info(class_name)
        # 바운딩박스
        draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=3)
        # 글자박스
        draw.rectangle([(x1, y1 - 20), (x1 + width, y1)], fill="white")
        draw.text((x1, y1 - 15), f'{class_name} {confidence : .2f}', fill="black", font=ImageFont.load_default(),
                  size=15)
    return image

# 메인화면이동
@app.get("/") # get방식의 요청 테스트용 메세지를 json 형식으로 반환
async def read_root():
    return {"message" : "Hello FastAPI"}

#이미지 받기
@app.post("/detect", response_model=DetectionResult)
async def detect_service(message: str = Form(...), file: UploadFile = File(...)):

    # 이미지 파일 열기
    image = Image.open(io.BytesIO(await file.read()))

    # 알파채널(A_필터)이 있다면 제거하고 RGB로 변환
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # 두 번째 예측 (이미지 객체 사용)
    img = np.array(image)  # 이미지를 numpy 배열로 변환
    result_image = model.predict(img, confidence=40, overlap=30).json()

    # 바운딩 박스그리기
    image = draw_bounding_box(image, result_image)

    # 이미지 파일을 읽고 Base64로 인코딩
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG") # 또는 원하는 형식으로 저장
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    logging.info("Image successfully encoded to Base64.")

    return DetectionResult(message=message, image=img_str)

###########################################################################
# 웹 실행_수동실행
if __name__ == "__main__": # uvicorn main:app인 경우 포트와 uvicorn 실행
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

###################################################################################

