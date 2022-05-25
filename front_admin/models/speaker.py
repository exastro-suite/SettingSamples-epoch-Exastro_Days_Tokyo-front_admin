#   Copyright 2022 NEC Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import json
import os
import requests
import traceback

from logging import getLogger

logger = getLogger(__name__)


def get_speakers(id_token):
    logger.debug("Method called.")

    base_url = _create_base_url()
    api_path = '/api/v1/speaker'
    header = _create_header(id_token)

    speakers = {}
    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        response = requests.get(base_url + api_path, headers=header)
        response.raise_for_status()

        speakers = response.json()
        #logger.debug("speakers: {}".format(json.dumps(speakers)))

    except Exception as e:
        logger.debug(e)
        logger.debug("traceback:" + traceback.format_exc())

        # todo

    return speakers

def get_speaker_detail(speaker_id, id_token):
    logger.debug("models.speaker.get_speaker_detail called.")

    base_url = _create_base_url()
    api_path = '/api/v1/speaker/{}'.format(speaker_id)
    header = _create_header(id_token)
    body = {}

    event_detail = {}
    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        response = requests.get(base_url + api_path, headers=header, data=json.dumps(body))
        response.raise_for_status()

        event_detail = response.json()

    except Exception as e:
        logger.debug(e)
        logger.debug("traceback:" + traceback.format_exc())

        raise

    return event_detail

def create_speaker(speaker_info, id_token):
    logger.debug("models.speaker.create_event called.")

    base_url = _create_base_url()
    api_path = '/api/v1/speaker/'
    header = _create_header(id_token)
    body = speaker_info

    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        response = requests.post(base_url + api_path, headers=header, data=json.dumps(body))
        response.raise_for_status()

    except Exception as e:
        logger.debug(e)
        logger.debug("traceback:" + traceback.format_exc())

        raise

    return None

def update_speaker(speaker_info, id_token):
    logger.debug("models.speaker.update_speaker called.")

    speaker_id = speaker_info['speaker_id']
    base_url = _create_base_url()
    api_path = '/api/v1/speaker/{}'.format(speaker_id)
    header = _create_header(id_token)
    body = speaker_info

    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        response = requests.put(base_url + api_path, headers=header, data=json.dumps(body))
        response.raise_for_status()

    except Exception as e:
        logger.debug(e)
        logger.debug("traceback:" + traceback.format_exc())

        raise

    return None

def delete_speaker(speaker_id, id_token):
    logger.debug("models.event.delete_speaker called.")

    base_url = _create_base_url()
    api_path = '/api/v1/speaker/{}'.format(speaker_id)
    header = _create_header(id_token)

    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        response = requests.delete(base_url + api_path, headers=header)
        response.raise_for_status()

    except Exception as e:
        logger.debug(e)
        logger.debug("traceback:" + traceback.format_exc())

        raise

    return None

def _create_header(id_token):
    # ヘッダ情報
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(id_token),
    }

    return header

def _create_base_url():

    protocol = os.environ['SERVICE_SPEAKER_PROTOCOL']
    host = os.environ['SERVICE_SPEAKER_HOST']
    port = os.environ['SERVICE_SPEAKER_PORT']

    return protocol + '://' + host + ':' + port
