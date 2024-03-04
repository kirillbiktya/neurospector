
from celery import Celery
from config import DB_URL
from database import SessionLocal, engine
from uuid import uuid4

from database import schemas, models

models.Base.metadata.create_all(bind=engine)


app = Celery(
    'yolo-backend',
    broker='pyamqp://guest@localhost//',
    backend='db+' + DB_URL
)


@app.task
def predict(image: schemas.Image):  # TODO
    db = SessionLocal()
    classes = db.query(models.Class.id).all()
    classes = [x[0] for x in classes]
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
