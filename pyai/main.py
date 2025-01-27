from function import *
import logging #로그
logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI, UploadFile, File, Form
app = FastAPI()

# 메인화면이동
@app.get("/") # get방식의 요청 테스트용 메세지를 json 형식으로 반환
async def read_root():
    return {"message" : "Hello FastAPI"}

# 이미지 받기
@app.post("/detect", response_model=DetectionResult)
async def detect_service(message : str = Form(...), file:UploadFile = File(...)):
    # 이미지를 읽어서 PIL 이미지로 반환
    image = Image.open(io.BytesIO(await file.read()))

    # 알파채널(A_필터)이 있다면 제거하고 RGB로 변환
    image = removal_filter(image)

    #예측(이미지 객체 이용)
    confidence = 40 #신뢰도
    overlap = 30    #오버랩
    result_image = model_predict(image, confidence, overlap)
    
    #바운딩박스 생성
    image = draw_bounding_box(image, result_image)

    # 이미지 결과를 base64로 인코딩
    img_str = encode_base64(image)

    return DetectionResult(message=message, image=img_str)

########################################################################
# 웹 실행_수동실행
if __name__ == "__main__": # uvicorn main:app인 경우 포트와 uvicorn 실행
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
########################################################################