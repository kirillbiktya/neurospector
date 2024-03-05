from typing import Optional

from pydantic import BaseModel, UUID4


class Class(BaseModel):
    id: int
    label: str


class Prediction(BaseModel):
    id: UUID4
    image_id: UUID4
    x1: int
    y1: int
    x2: int
    y2: int
    class_id: int
    confidence: float

    # image: Image | None
    predicted_class: Class | None


class Image(BaseModel):
    id: UUID4
    path: str
    processed: bool = False
    predictions: list[Prediction] = []
