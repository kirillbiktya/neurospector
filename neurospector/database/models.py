from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, Identity
from sqlalchemy.orm import relationship

from neurospector.database import Base


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, Identity(start=0, cycle=False), primary_key=True, index=True, unique=True)
    label = Column(String, index=True)

    predictions = relationship("Prediction", back_populates="predicted_class")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Identity(start=0, cycle=False), primary_key=True, index=True, unique=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    sessions = relationship("Session")
    images = relationship("Image")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, Identity(start=0, cycle=False), primary_key=True, index=True, unique=True)
    image_width = Column(Integer)
    image_height = Column(Integer)
    fps = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    is_active = Column(Boolean, default=False)

    images = relationship("Image")
    user = relationship("User", back_populates="sessions")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, Identity(start=0, cycle=False), primary_key=True, index=True, unique=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), index=True)
    session_sequence_id = Column(Integer)
    bucket_name = Column(String)
    key = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    session = relationship("Session", back_populates="images")
    predictions = relationship("Prediction")
    user = relationship("User", back_populates="images")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, Identity(start=0, cycle=False), primary_key=True, index=True, unique=True)
    image_id = Column(Integer, ForeignKey("images.id"), index=True)
    x1 = Column(Integer)
    y1 = Column(Integer)
    x2 = Column(Integer)
    y2 = Column(Integer)
    class_id = Column(Integer, ForeignKey("classes.id"), index=True)
    confidence = Column(Float, index=True)

    image = relationship("Image", back_populates="predictions")
    predicted_class = relationship("Class")
