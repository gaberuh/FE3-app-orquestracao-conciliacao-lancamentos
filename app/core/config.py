import os
import logging
from dotenv import load_dotenv
import boto3

load_dotenv()


class Settings:
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    ATHENA_OUTPUT_S3 = os.getenv("ATHENA_OUTPUT_S3")
    SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

    INPUT_FILE = os.getenv("INPUT_FILE")
    CAPACITY_LIMIT = int(os.getenv("CAPACITY_LIMIT", "1000000"))

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


settings = Settings()


# ===========================
# LOGGER GLOBAL
# ===========================
def get_logger():
    logger = logging.getLogger("conciliacao-binner")

    if not logger.handlers:
        logger.setLevel(settings.LOG_LEVEL)

        handler = logging.StreamHandler()
        handler.setLevel(settings.LOG_LEVEL)

        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = get_logger()


# ===========================
# AWS Clients
# ===========================
def get_athena_client():
    return boto3.client(
        "athena",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def get_sqs_client():
    return boto3.client(
        "sqs",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
