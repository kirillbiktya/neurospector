import json
from random import randint

from fastapi import Depends, FastAPI, Response, Header
from sqlalchemy.orm import Session

from neurospector.database import SessionLocal, engine
from neurospector.database import crud
from neurospector.database import models, schemas
from neurospector.worker import app as celery_app

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/new_session")
def get_new_session(w: int, h: int, fps: int, username: str = Header(), password: str = Header(),
                    db: Session = Depends(get_db)):  # TODO: change authentication mechanism (tokens?)
    user = db.query(models.User).filter(models.User.username == username and models.User.password == password).first()
    if user is None:
        return Response("wrong credentials", 400)

    port = randint(9000, 9999)  # TODO: add temporary db entry about used ports to avoid doubles
    db_session = models.Session(image_width=w, image_height=h, fps=fps, user_id=user.id)
    db.add(db_session)
    db.commit()
    celery_app.send_task("neurospector.worker.cpu_worker.run_session", args=[db_session.id, port], queue="cpu")

    return Response(json.dumps({"session": db_session.id, "port": port}), 200)


@app.get("/predictions", response_model=list[schemas.Prediction])
def get_predictions_for_image(image_id: int, db: Session = Depends(get_db)):
    return crud.get_predictions_by_image_id(db, image_id)


@app.get("/setup")
def setup(db: Session = Depends(get_db)):  # TODO: DO NOT USE IT IN REAL! separate this from production code
    for db_class in [
        "opora_double_side", "opora_single_side", "opora_vysoko", "light_bulb_good", "light_bulb_defective"
    ]:
        db.add(models.Class(label=db_class))
    db.add(models.User(username="kirill", password="kirill"))
    db.commit()
    return Response("ok", 200)
