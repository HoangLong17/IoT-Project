import time
from IOT.celery import app
from .ai import face_recognition_ai
import time

@app.task
def face_ai(path_image):
    return face_recognition_ai(path_image)
    


@app.task
def task_demo():
    print("start demo--------------------------")
    time.sleep(15)
    print("end demo----------------------------")
    return True

