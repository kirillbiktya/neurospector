from base64 import b64decode

from config import NN_MODEL_PATH
from neurospector.database import SessionLocal
from neurospector.database import models, crud
from neurospector.ml.yolo import Detector
from neurospector.worker import app

detector = Detector(NN_MODEL_PATH)
db = SessionLocal()

classes = crud.get_classes(db)
classes = [x.id for x in classes]
print(classes)


@app.task(queue="gpu")
def predict_s3(image_id: int, image_key: str):
    result = detector.detect_from_s3(image_key, classes)

    for i in result:
        db_prediction = models.Prediction(
            image_id=image_id,
            x1=i['coords']['x1'],
            x2=i['coords']['x2'],
            y1=i['coords']['y1'],
            y2=i['coords']['y2'],
            class_id=i['class'],
            confidence=i['confidence']
        )
        db.add(db_prediction)
    db.commit()


@app.task(queue="gpu")
def predict_local(image_id: int, image_bytes_base64):
    image_bytes = b64decode(image_bytes_base64)

    result = detector.detect_from_bytes(image_bytes, classes)

    for i in result:
        db_prediction = models.Prediction(
            image_id=image_id,
            x1=i['coords']['x1'],
            x2=i['coords']['x2'],
            y1=i['coords']['y1'],
            y2=i['coords']['y2'],
            class_id=i['class'],
            confidence=i['confidence']
        )
        db.add(db_prediction)
    db.commit()
