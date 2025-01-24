import os

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form

import io
import base64
import numpy as np

from pydantic import BaseModel
from PIL import Image, ImageDraw

import logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

#.env 보안코드 호출
load_dotenv() 
api_key = os.getenv("ROBOFLOW_API_KEY")
workspace = os.getenv("workspace")
project = os.getenv("project")
version = os.getenv("version")

#roboflow_model 호출
from roboflow import Roboflow
rf = Roboflow(api_key=api_key)
project = rf.workspace(workspace).project(project)
version = project.version(version)
# dataset = version.download("yolov11")
model = version.model

# 메시지출력 및 이미지 출력함수
class DetectionResult(BaseModel):
    message : str
    image : str

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
        draw.text((x1, y1-15), f'{class_name} {confidence : .2f}', fill="black", size=15)
    return image

# 메인화면이동
@app.get("/") # get방식의 요청 테스트용 메세지를 json 형식으로 반환
async def read_root():
    return {"message" : "Hello FastAPI"}

# 이미지 받기
@app.post("/detect", response_model=DetectionResult)
async def detect_service(message : str = Form(...), file:UploadFile = File(...)):
    # 이미지를 읽어서 PIL 이미지로 반환
    image = Image.open(io.BytesIO(await file.read()))

    #알파채널(A_필터)이 있다면 제거하고 RGB로 변환
    if image.mode != 'RGB':
        image = image.convert('RGB')

    #예측(이미지 객체 이용)
    img = np.array(image) #이미지 numpy 배열 반환
    result_image = model.predict(img, confidence=40, overlap=30).json()

    image = draw_bounding_box(image, result_image)

    # 이미지 결과를 base64로 인코딩
    buffered = io.BytesIO()
    image.save(buffered, format='JPEG') #JPEG로 이미지저장
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return DetectionResult(message=message, image=img_str)

########################################################################
# 웹 실행_수동실행
if __name__ == "__main__": # uvicorn main:app인 경우 포트와 uvicorn 실행
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
########################################################################