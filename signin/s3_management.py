import random
import string
import os
import boto3
import io
from datetime import datetime
from PIL import Image
from aws3 import S3_ACCESS_KEY, S3_BUCKET, S3_CLOUDFRONT_URL, S3_REGION, S3_SECRET_KEY

s3_access_key = S3_ACCESS_KEY
s3_secret_key = S3_SECRET_KEY
s3_region = S3_REGION
s3_bucket_name = S3_BUCKET
s3_cloudfront_url = S3_CLOUDFRONT_URL


S3_SESSION = boto3.Session(
    aws_access_key_id=s3_access_key,
    aws_secret_access_key=s3_secret_key,
    region_name=s3_region,
)
S3_CLIENT = S3_SESSION.client("s3")


def unix_timestamp(timestamp: datetime = None, round_off: bool = False):
    timestamp = datetime.datetime.now() if timestamp is None else timestamp
    unix_timestamp = int(
        datetime.datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S.%f").timestamp()
    )
    if round_off:
        dt_object = datetime.datetime.fromtimestamp(unix_timestamp)
        end_of_day = datetime.datetime.combine(dt_object, datetime.time(23, 59, 59))
        return int(end_of_day.timestamp())
    return unix_timestamp


def generate_random_string(length):
    letters = string.ascii_letters
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string


def s3_image_upload(request, image_data, folder_name=None, content_type=None):
    if image_data is None:
        return None

    current_month = datetime.now().month
    current_year = datetime.now().year

    if folder_name:
        folder_name = str(folder_name).replace(" ", "-")
        folder_name = (
            f"{current_month}-{current_year}/{folder_name}/{request.user.username}"
        )
    else:
        folder_name = f"{current_month}-{current_year}/{request.user.username}"

    if not content_type:
        content_type = image_data.content_type
        # image_data.seek(0)

    image_extension = content_type.split("/")[-1]
    file_name = generate_random_string(7)
    image_name = f"{file_name}.{image_extension}"

    S3_CLIENT.put_object(
        Bucket=s3_bucket_name,
        Key=f"{folder_name}/{image_name}",
        Body=image_data,
        ACL="public-read",
        ContentType=content_type,
    )
    # try:
    #     with Image.open(image_data) as img:
    #         size = (128, 128)
    #         img.thumbnail(size)
    #         image_data = io.BytesIO()
    #         try:
    #             img.save(image_data, format=image_extension)
    #         except:
    #             img.save(image_data, format="JPEG")
    #         image_data.seek(0)

    #         S3_CLIENT.put_object(
    #             Bucket=s3_bucket_name,
    #             Key=f"thumbnails/{folder_name}/{image_name}",
    #             Body=image_data,
    #             ACL="private",
    #             ContentType=content_type,
    #         )
    # except:
    #     print("thumbnail error")

    image_url = f"{s3_cloudfront_url}/{folder_name}/{image_name}"
    print("image_url", image_url)
    return image_url


def delete_file_from_s3(file_key):
    image_domain = s3_cloudfront_url
    file_key = file_key.replace(image_domain + "/", "")

    response = S3_CLIENT.delete_object(Bucket=s3_bucket_name, Key=file_key)
    return response
