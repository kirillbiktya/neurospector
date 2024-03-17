import boto3

from config import YC_KEY_ID, YC_KEY, YC_OBJECT_STORAGE_BUCKET

session = boto3.session.Session(
    region_name="ru-central1",
    aws_access_key_id=YC_KEY_ID,
    aws_secret_access_key=YC_KEY
)
client = session.client(
    's3',
    endpoint_url="https://storage.yandexcloud.net"
)


def upload_file(key: str, contents):
    client.put_object(Bucket=YC_OBJECT_STORAGE_BUCKET, Key=key, Body=contents, StorageClass="STANDARD")


def get_file(key: str) -> bytes:
    obj = client.get_object(Bucket=YC_OBJECT_STORAGE_BUCKET, Key=key)
    data = obj["Body"].read()
    obj["Body"].close()
    return data
