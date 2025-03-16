import logging
import os
import sys
import time

from func_timeout import func_timeout
from redis import Redis

from lib.anthropic import describe_via_anthropic
from lib.consts import REDIS_DB, REDIS_DATA_KEY
from lib.ha import get_ha_sensor
from lib.image import fetch_latest_frame, resize_image, encode_image_to_base64
from lib.openai import describe_via_openai

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel('CRITICAL')
logging.getLogger('httpx').propagate = False

HLS_STREAM = os.getenv('HLS_STREAM')
AI_MODEL = os.getenv('AI_MODEL', 'claude-3-7-sonnet-latest')
AI_API_KEY = os.getenv('AI_API_KEY')
AI_BASE_URL = os.getenv('AI_BASE_URL')
WEBCAM_LOCATION = os.getenv('WEBCAM_LOCATION')
WEBCAM_VIEW_DESCRIPTION = os.getenv('WEBCAM_VIEW_DESCRIPTION')
HA_ACCESS_TOKEN = os.getenv('HA_ACCESS_TOKEN')
HA_BASE_URL = os.getenv('HA_BASE_URL')
HA_TEMPERATURE_SENSOR = os.getenv('HA_TEMPERATURE_SENSOR')

if not HLS_STREAM or not AI_API_KEY or not WEBCAM_LOCATION or not WEBCAM_VIEW_DESCRIPTION or not HA_ACCESS_TOKEN or not HA_BASE_URL or not HA_TEMPERATURE_SENSOR:
    logging.critical('Must set HLS_STREAM, AI_API_KEY, WEBCAM_LOCATION, WEBCAM_VIEW_DESCRIPTION, HA_ACCESS_TOKEN, HA_BASE_URL, HA_TEMPERATURE_SENSOR environment variables')
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

        logging.info(f'Sending image to {"Anthropic" if "claude" in AI_MODEL else "OpenAI"} for description...')
        last_description: bytes = redis.get('webcam_intelligence_last')
        last_description_s = None
        if last_description:
            last_description_s = last_description.decode('utf-8')

        if 'claude' in AI_MODEL:
            provider = describe_via_anthropic
        else:
            provider = describe_via_openai

        description = func_timeout(120, provider, (image_base64, AI_API_KEY, AI_MODEL, AI_BASE_URL, WEBCAM_LOCATION, WEBCAM_VIEW_DESCRIPTION, temp, temp_unit, last_description_s))
        redis.set('webcam_intelligence_last', description)
        d = description.replace('\n', ' ')
        logging.info(f'AI wrote a {len(description)} character summary: "{d}"')

        redis.set(REDIS_DATA_KEY, description)

        logging.info(f'Sleeping {SLEEP_MINUTES} minutes...')
        time.sleep(SLEEP_MINUTES * 60)


if __name__ == '__main__':
    main()
