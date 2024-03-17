from base64 import b64encode, b64decode
from io import BytesIO
from time import sleep
from uuid import uuid4

import cupy as cp
import numpy as np
from PIL import Image

import neurospector.ffmpeg as ff
import neurospector.s3 as s3
from config import YC_OBJECT_STORAGE_BUCKET, LOCAL_PREDICT
from neurospector.database import SessionLocal
from neurospector.database import models, crud
from neurospector.worker import app

db = SessionLocal()


@app.task(queue="cpu")
def run_session(session_id: int, port: int):  # TODO: move to gpu_worker because of cupy usage
    session = crud.get_session_by_id(db, session_id)

    frame_queue = ff.Queue()
    ffmpeg_thread = ff.FFmpegServer(port, session.image_height, session.image_width, session.fps)
    enqueuer_thread = ff.FFmpegFrameEnqueuer(ffmpeg_thread, frame_queue)

    ffmpeg_thread.start()
    sleep(1)  # wait for ffmpeg opens stdout
    enqueuer_thread.start()

    session.is_active = True
    db.commit()

    queue_iterator = ff.frame_generator(frame_queue)
    session_sequence_id = 0

    # TODO: add idle timeout

    for entry in queue_iterator:
        # бутылочное горлышко при высоких разрешениях
        cpimg = cp.frombuffer(entry, dtype=np.uint8).reshape((session.image_height, session.image_width, 3))
        npimg = cp.asnumpy(cpimg)

        im = Image.fromarray(npimg)
        im_bytes = BytesIO()
        im.save(im_bytes, format='JPEG')
        im_bytes_base64 = b64encode(im_bytes.getvalue()).decode('utf-8')

        app.send_task("neurospector.worker.cpu_worker.create_image",
                      args=[session.id, session_sequence_id, session.user_id, im_bytes_base64], queue="cpu")

        session_sequence_id += 1


@app.task(queue="cpu")
def create_image(session_id: int, session_sequence_id: int, user_id: int, image_bytes_base64):
    image_key = uuid4()
    image_bytes = b64decode(image_bytes_base64)
    db_image = models.Image(session_id=session_id, session_sequence_id=session_sequence_id,
                            bucket_name=YC_OBJECT_STORAGE_BUCKET, key=image_key.hex + '.jpg', user_id=user_id)
    if LOCAL_PREDICT:
        db.add(db_image)
        db.commit()
        # TODO: нужно какое-то локальное хранилище. S3?))))
        # app.send_task("neurospector.worker.cpu_worker.upload_image_to_s3", args=[db_image.key, image_bytes_base64],
        #               queue="cpu")
        app.send_task("neurospector.worker.gpu_worker.predict_local", args=[db_image.id, image_bytes_base64],
                      queue="gpu")
    else:
        db.add(db_image)
        s3.upload_file(db_image.key.hex, image_bytes)
        db.commit()
        app.send_task("neurospector.worker.gpu_worker.predict_s3", args=[db_image.id, db_image.key.hex], queue="gpu")


@app.task(queue="cpu")
def upload_image_to_s3(image_key: str, image_bytes_base64):
    image_bytes = b64decode(image_bytes_base64)
    s3.upload_file(image_key, image_bytes)
