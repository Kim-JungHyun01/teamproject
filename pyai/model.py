from dotenv import load_dotenv
import os
from roboflow import Roboflow

def load_model():
    #.env 보안코드 호출
    load_dotenv()
    api_key = os.getenv("ROBOFLOW_API_KEY")
    workspace = os.getenv("workspace")
    project = os.getenv("project")
    version = os.getenv("version")

    #roboflow_model 호출
    rf = Roboflow(api_key=api_key)                      #roboflow 접속
    project = rf.workspace(workspace).project(project)  #훈련 workspase선택
    version = project.version(version)                  #훈련모델버전선택
    # dataset = version.download("yolov11")             #데이터베이스다운
    model = version.model
    return model