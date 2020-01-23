import traceback
import json
import requests

from kafka import KafkaConsumer

from kerlescan.inventory_service_interface import fetch_systems_with_profiles

from system_profile_archiver import logging, metrics, config

logger = logging.initialize_logging()


def main():
    logger.info("starting listener")

    consumer = init_consumer()

    counters = {
        "inventory_service_requests": metrics.inventory_service_requests,
        "inventory_service_exceptions": metrics.inventory_service_exceptions,
        "systems_compared_no_sysprofile": metrics.inventory_service_no_profile,
    }

    while True:
        for data in consumer:
            logger.info("consuming message")
            try:
                inventory_uuid = data.value["host"]["id"]
                identity = data.value["platform_metadata"]["b64_identity"]

                # fetch system from inventory
                # TODO: handle case w/ missing system
                systems = fetch_systems_with_profiles(
                    [inventory_uuid], identity, logger, counters
                )
                system = systems[0]["system_profile"]
                system["system_profile_exists"] = True
                system["display_name"] = systems[0]["display_name"]

                # create historical system profile
                profile = {"inventory_id": inventory_uuid, "profile": system}
                headers = {
                    "x-rh-identity": identity,
                    "content-type": "application/json",
                }

                result = requests.post(
                    config.HISTORICAL_SYS_PROFILE_URL,
                    data=json.dumps(profile),
                    headers=headers,
                )
                logger.info("result of POST: %s" % result.status_code)

            except Exception:
                logger.exception("An error occurred during message processing")


def init_consumer():
    consumer = KafkaConsumer(
        config.CONSUME_TOPIC,
        bootstrap_servers=config.BOOTSTRAP_SERVERS,
        group_id=config.GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        retry_backoff_ms=1000,
        consumer_timeout_ms=200,
    )
    return consumer


if __name__ == "__main__":
    try:
        main()
    except Exception:
        the_error = traceback.format_exc()
        logger.exception(f"system-profile-archiver failed with Error: {the_error}")
