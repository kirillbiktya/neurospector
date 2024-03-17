from typing import Type

from sqlalchemy.orm import Session

from neurospector.database import models, schemas
from neurospector.database.models import Class


def create_class(db: Session, _class: models.Class) -> models.Class:
    db_class = models.Class(**_class.dict())
    db.add(db_class)
    db.commit()
    return db_class


def get_class(db: Session, class_id: int | None, label: str | None) -> models.Class | None:
    return db.query(models.Class).filter(
        (class_id is not None and models.Class.id == class_id) or
        (label is not None and models.Class.label == label)
    ).first()


def get_classes(db: Session) -> list[Type[Class]]:
    return db.query(models.Class).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User | None:
    db_user = models.User(**user.dict())
    if db.query(models.User).filter(models.User.username == db_user.username).first():
        return None

    db.add(db_user)
    db.commit()
    return db_user


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def auth_user(db: Session, credentials: schemas.UserCredentials) -> bool:
    return db.query(models.User).filter(
        models.User.username == credentials.username and models.User.password == credentials.password
    ).first() is not None


def create_session(db: Session, session: schemas.Session) -> models.Session:
    db_session = models.Session(**session.dict())
    db.add(db_session)
    db.commit()
    return db_session


def get_session_by_id(db: Session, session_id: int) -> models.Session | None:
    return db.query(models.Session).filter(models.Session.id == session_id).first()


def get_sessions_by_user_id(db: Session, user_id: int) -> list[Type[models.Session]]:
    return db.query(models.Session).filter(models.Session.user_id == user_id).all()


def create_image(db: Session, image: schemas.Image) -> models.Image:
    db_image = models.Image(**image.dict())
    db.add(db_image)
    db.commit()
    return db_image


def get_image_by_id(db: Session, image_id: int) -> models.Image | None:
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def get_images_by_session_id(db: Session, session_id: int) -> list[Type[models.Image]]:
    return db.query(models.Image).filter(models.Image.session_id == session_id).all()


def create_prediction(db: Session, prediction: schemas.Prediction) -> models.Prediction:
    db_prediction = models.Prediction(**prediction.dict())
    db.add(db_prediction)
    db.commit()
    return db_prediction


def get_prediction_by_id(db: Session, prediction_id: int) -> models.Prediction | None:
    return db.query(models.Prediction).filter(models.Prediction.id == prediction_id).first()


def get_predictions_by_image_id(db: Session, image_id: int) -> list[Type[models.Prediction]]:
    return db.query(models.Prediction).filter(models.Prediction.image_id == image_id).all()
