# General config vars
DEV = True
VERSION = "1.0a1"
LOCAL_PREDICT = True

# Yandex CLoud config vars
YC_KEY_ID = ""
YC_KEY = ""
YC_OBJECT_STORAGE_BUCKET = ""

# Postgres config vars
DB_ADDRESS = ""
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_URL = "postgresql://{0}:{1}@{2}/{3}".format(DB_USER, DB_PASSWORD, DB_ADDRESS, DB_NAME)

# RabbitMQ config vars
# TODO

# YOLO config vars
NN_MODEL_PATH = 'model.pt'
