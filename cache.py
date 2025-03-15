import logging
import os
import sys
import time

from redis import Redis

from lib.anthropic import describe_image_via_ai
from lib.consts import REDIS_DB, REDIS_DATA_KEY
from lib.ha import get_ha_sensor
from lib.image import fetch_latest_frame, resize_image, encode_image_to_base64

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel('CRITICAL')
logging.getLogger('httpx').propagate = False

HLS_STREAM = os.getenv('HLS_STREAM')
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3-7-sonnet-latest')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
ANTHROPIC_BASE_URL = os.getenv('ANTHROPIC_BASE_URL')
WEBCAM_LOCATION = os.getenv('WEBCAM_LOCATION')
WEBCAM_VIEW_DESCRIPTION = os.getenv('WEBCAM_VIEW_DESCRIPTION')
HA_ACCESS_TOKEN = os.getenv('HA_ACCESS_TOKEN')
HA_BASE_URL = os.getenv('HA_BASE_URL')
HA_TEMPERATURE_SENSOR = os.getenv('HA_TEMPERATURE_SENSOR')

if not HLS_STREAM or not ANTHROPIC_API_KEY or not WEBCAM_LOCATION or not WEBCAM_VIEW_DESCRIPTION or not HA_ACCESS_TOKEN or not HA_BASE_URL or not HA_TEMPERATURE_SENSOR:
    logging.critical('Must set HLS_STREAM, ANTHROPIC_API_KEY, WEBCAM_LOCATION, WEBCAM_VIEW_DESCRIPTION, HA_ACCESS_TOKEN, HA_BASE_URL, HA_TEMPERATURE_SENSOR environment variables')
    sys.exit(1)

SLEEP_MINUTES = 15


def main():
    redis = Redis(db=REDIS_DB)
    while True:
        logging.info('Fetching temperature data...')
        temp, temp_unit = get_ha_sensor(HA_ACCESS_TOKEN, HA_BASE_URL, HA_TEMPERATURE_SENSOR)

        logging.info('Fetching latest frame from the HLS stream...')
        frame = fetch_latest_frame(HLS_STREAM)
        resized_image = resize_image(frame)
        image_base64 = encode_image_to_base64(resized_image)

        logging.info('Sending image to the AI for description...')
        description = describe_image_via_ai(image_base64, ANTHROPIC_API_KEY, ANTHROPIC_MODEL, ANTHROPIC_BASE_URL, WEBCAM_LOCATION, WEBCAM_VIEW_DESCRIPTION, temp, temp_unit)
        logging.info(f'AI wrote a {len(description)} character summary.')

        redis.set(REDIS_DATA_KEY, description)

        logging.info(f'Sleeping {SLEEP_MINUTES} minutes...')

        time.sleep(SLEEP_MINUTES * 60)


if __name__ == '__main__':
    main()
