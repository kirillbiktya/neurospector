from pydantic import UUID4
from sqlalchemy.orm import Session

from database import models, schemas


def create_class(db: Session, _class: schemas.Class):
    db_class = models.Class(**_class.dict())
    db.add(db_class)
    db.commit()
    return db_class


def get_class(db: Session, class_id: int | None, label: str | None):
    return db.query(models.Class).filter(
        (class_id is not None and models.Class.id == class_id) or
        (label is not None and models.Class.label == label)
    ).first()


def get_classes(db: Session):
    return db.query(models.Class).all()


def create_image(db: Session, image: schemas.Image):
    db_image = models.Image(**image.dict())
    db.add(db_image)
    db.commit()
    return db_image


def get_image(db: Session, image_id: UUID4):
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def mark_image_as_processed(db: Session, image_id: UUID4):
    db.query(models.Image).filter(models.Image.id == image_id).update({"processed": True})
    db.commit()
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def create_prediction(db: Session, prediction: schemas.Prediction):
    db_prediction = models.Prediction(**prediction.dict())
    db.add(db_prediction)
    db.commit()
    return db_prediction


def get_prediction(db: Session, prediction_id: UUID4):
    return db.query(models.Prediction).filter(models.Prediction.id == prediction_id).first()


def get_predictions_by_image(db: Session, image_id: UUID4):
    return db.query(models.Prediction).filter(models.Prediction.image_id == image_id).all()
