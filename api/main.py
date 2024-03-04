from fastapi import Depends, FastAPI, HTTPException, File, UploadFile, Response
from sqlalchemy.orm import Session
from uuid import uuid4, UUID

from database import crud
from database import models, schemas
from database import SessionLocal, engine
from worker.main import celery_app

from config import UPLOAD_DIRECTORY

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/image", response_model=schemas.Image)
def create_image(file: UploadFile, db: Session = Depends(get_db)):  # TODO: может, все же лучше возвращать таск?
    image_id = uuid4()
    db_image = schemas.Image(id=image_id, path=UPLOAD_DIRECTORY + image_id + '.jpg')

    try:
        contents = file.file.read()
        with open(db_image.path, 'wb') as f:
            f.write(contents)
    except Exception as e:
        return Response("Error encountered: " + str(e), 500)
    finally:
        file.file.close()

    crud.create_image(db, db_image)
    celery_app.send_task("worker.predict", args=[db_image])

    return db_image


@app.get("/predictions", response_model=list[schemas.Prediction])
def get_predictions_for_image(image_id: str, db: Session = Depends(get_db)):
    return crud.get_predictions_by_image(db, UUID(image_id))


@app.get("/setup")
def setup(db: Session = Depends(get_db)):
    crud.create_class(db, schemas.Class(id=0, label="opora_double_side"))
    crud.create_class(db, schemas.Class(id=1, label="opora_single_side"))
    crud.create_class(db, schemas.Class(id=2, label="opora_vysoko"))
    crud.create_class(db, schemas.Class(id=3, label="light_bulb_good"))
    crud.create_class(db, schemas.Class(id=4, label="light_bulb_defective"))
    return Response("ok", 200)
