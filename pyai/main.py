# 라이브러리 설치

# pip install fastapi uvicorn pydantic Pillow numpy requests

# fastapi  : 비동기 웹프레임워크, 자동으로 OpenAPI  문서생성
# uvicorn  : 고성능 비동기 서버 = 톰캑, ASGI 표준 지원
# pydatic  : 데이터검증, 직렬화, 타입힌팅, 설정관리
# Pillow   : 이미지 열기, 저장, 변환, 다양한 이미지 처리
# numpy    : 수치계산, 배열 및 행렬 연산, 다양한 수학함수
# requests : 간단한 http 요청 및 응당처리

# pip install ultralytics opencv-python python-multipart

# ultralytics      : YOLO8 객체 탐지 모델제공
# opencv-python    : 이미지 및 비디오 처리, 컴퓨터 비전 기능(roboflow 대체)
# python-multipart : multipart 폼 데이터를 파싱하기 위함

# cmd 실행
# uvicorn main:app --reload
##########################################################################

# 라우칭, 파일업로드, 폼데이터처리
from fastapi import FastAPI, UploadFile, File, Form


app = FastAPI()

# 웹 실행_수동실행
if __name__ == "__main__": # uvicorn main:app인 경우 포트와 uvicorn 실행
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)