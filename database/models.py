from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, UUID
from sqlalchemy.orm import relationship

from . import Base


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    label = Column(String, index=True)

    predictions = relationship("Prediction", back_populates="predicted_class")


class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True)
    path = Column(String)
    processed = Column(Boolean, default=False)

    predictions = relationship("Prediction", back_populates="image")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True)
    image_id = Column(UUID(as_uuid=True), ForeignKey("images.id"), index=True)
    x1 = Column(Integer)
    y1 = Column(Integer)
    x2 = Column(Integer)
    y2 = Column(Integer)
    class_id = Column(Integer, ForeignKey("classes.id"), index=True)
    confidence = Column(Float, index=True)

    image = relationship("Image", back_populates="predictions")
    predicted_class = relationship("Class")
