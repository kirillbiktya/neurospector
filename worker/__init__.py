from celery import Celery

from config import DB_URL

app = Celery(
    'yolo-backend',
    broker='pyamqp://guest@localhost//',
    backend='db+' + DB_URL
)
