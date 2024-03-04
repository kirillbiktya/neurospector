from . import app
from ml.yolo import Detector
from config import NN_MODEL_PATH

celery_app = app

detector = Detector(NN_MODEL_PATH)