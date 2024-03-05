from uuid import uuid4

from config import NN_MODEL_PATH
from database import SessionLocal, engine
from database import schemas, models
from ml.yolo import Detector
from . import app

models.Base.metadata.create_all(bind=engine)

detector = Detector(NN_MODEL_PATH)


@app.task
def predict(image_id: str):
    db = SessionLocal()
    classes = db.query(models.Class.id).all()
    classes = [x[0] for x in classes]
    image = db.query(models.Image).filter(models.Image.id == image_id).first()
    result = detector.detect(image.path, classes)
    for i in result:
        db_prediction = models.Prediction(
            id=uuid4(),
            image_id=image.id,
            x1=i['coords']['x1'],
            x2=i['coords']['x2'],
            y1=i['coords']['y1'],
            y2=i['coords']['y2'],
            class_id=i['class'],
            confidence=i['confidence']
        )
        db.add(db_prediction)
    db.commit()
    return len(result)
