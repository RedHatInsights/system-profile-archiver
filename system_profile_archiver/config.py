import os
import logging

APP_NAME = os.getenv("APP_NAME", "system-profile-archiver")
AWS_ACCESS_KEY_ID = os.getenv("CW_AWS_ACCESS_KEY_ID", None)
AWS_REGION_NAME = os.getenv("CW_AWS_REGION_NAME", "us-east-1")
AWS_SECRET_ACCESS_KEY = os.getenv("CW_AWS_SECRET_ACCESS_KEY", None)
BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "kafka:29092").split(",")
CONSUME_TOPIC = os.getenv("CONSUME_TOPIC", "platform.inventory.host-egress")
GROUP_ID = os.getenv("GROUP_ID", APP_NAME)
HISTORICAL_SYS_PROFILE_URL = os.getenv(
    "HISTORICAL_SYS_PROFILE_URL", "historical_sys_profile_url_not_set"
)
LOG_GROUP = os.getenv("LOG_GROUP", "platform-dev")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

DB_USER = os.getenv("HSP_DB_USER", "insights")
DB_PORT = os.getenv("HSP_DB_PORT", "5432")
DB_PASSWORD = os.getenv("HSP_DB_PASS", "insights")
DB_HOST = os.getenv("HSP_DB_HOST", "localhost")
DB_NAME = os.getenv("HSP_DB_NAME", "insights")

logger = logging.getLogger(APP_NAME)


def log_config():
    import sys

    for k, v in sys.modules[__name__].__dict__.items():
        if k == k.upper():
            if "AWS" in k.split("_"):
                continue
            logger.info("Using %s: %s", k, v)


def get_namespace():
    try:
        with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
            namespace = f.read()
        return namespace
    except EnvironmentError:
        logger.info("Not running in openshift")


NAMESPACE = get_namespace()
