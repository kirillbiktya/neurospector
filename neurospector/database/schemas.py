from pydantic import BaseModel


class Class(BaseModel):
    id: int
    label: str


class User(BaseModel):
    id: int
    username: str


class UserCreate(User):
    password: str


class UserCredentials(BaseModel):
    username: str
    password: str


class Session(BaseModel):
    id: int
    image_width: int
    image_height: int
    fps: int
    user_id: int
    is_active: bool


class Image(BaseModel):
    id: int
    session_id: int
    session_sequence_id: int
    bucket_name: str
    key: str


class Prediction(BaseModel):
    id: int
    image_id: int
    x1: int
    y1: int
    x2: int
    y2: int
    class_id: int
    confidence: float
