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


def get_events(id_token):
    logger.debug("models.event.get_events called.")

    base_url = _create_base_url()
    api_path = '/api/v1/event'
    header = _create_header(id_token)
    body = {}

    event_list = []
    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        response = requests.get(base_url + api_path, headers=header, data=json.dumps(body))
        response.raise_for_status()

        event_list = response.json()

    except Exception as e:
        logger.debug(e)
        logger.debug("traceback:" + traceback.format_exc())

        # todo

    return event_list

def get_event_detail(event_id, id_token):
    logger.debug("models.event.get_event_detail called.")

    base_url = _create_base_url()
    api_path = '/api/v1/event/{}'.format(event_id)
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

def get_timetable(event_id, user_id = None, kind_of_sso = None, id_token = None):
    logger.debug("models.event.get_timetable called.")

    base_url = _create_base_url()
    api_path = '/api/v1/event/{}/timetable'.format(event_id)
    header = _create_header(id_token)
    params = {}

    if user_id:
        params['user_id'] = user_id
    if kind_of_sso:
        params['kind_of_sso'] = kind_of_sso

    event_timetable = {}
    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        response = requests.get(base_url + api_path, headers=header, params=params)
        response.raise_for_status()

        event_timetable = response.json()

    except Exception as e:
        logger.debug(e)
        logger.debug("traceback:" + traceback.format_exc())

        # todo

    return event_timetable

def get_master(id_token):
    logger.debug("models.event.get_master called.")

    base_url = _create_base_url()
    api_path = '/api/v1/master'
    header = _create_header(id_token)
    body = {}

    master = {}
    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        # response = requests.get(base_url + api_path, headers=header, data=json.dumps(body))
        # if response.status_code != 200:
        #     raise Exception(response)

        # master = response.json()

        master = {
            "block": ['A', 'B', 'C', 'D', ],
            "class": ['9', '10', '11', '12', '13', '14', '15', '16', '17', ],
        }

    except Exception as e:
        logger.debug(e)
        logger.debug("traceback:" + traceback.format_exc())

        # todo

    return master

def create_event(event_info, id_token):
    logger.debug("models.event.create_event called.")

    base_url = _create_base_url()
    api_path = '/api/v1/event/'
    header = _create_header(id_token)
    body = event_info

    #event_detail = {}
    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        response = requests.post(base_url + api_path, headers=header, data=json.dumps(body))
        response.raise_for_status()

        #event_detail = response.json()

    except Exception as e:
        logger.debug(e)
        logger.debug("traceback:" + traceback.format_exc())

        raise

    return None

def update_event(event_info, id_token):
    logger.debug("models.event.update_event called.")

    event_id = event_info['event_id']
    base_url = _create_base_url()
    api_path = '/api/v1/event/{}'.format(event_id)
    header = _create_header(id_token)
    body = event_info

    #event_detail = {}
    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        response = requests.put(base_url + api_path, headers=header, data=json.dumps(body))
        response.raise_for_status()

        #event_detail = response.json()

    except Exception as e:
        logger.debug(e)
        logger.debug("traceback:" + traceback.format_exc())

        raise

    return None

def delete_event(event_id, id_token):
    logger.debug("models.event.delete_event called.")

    base_url = _create_base_url()
    api_path = '/api/v1/event/{}'.format(event_id)
    header = _create_header(id_token)
    body = {}

    #event_detail = {}
    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        response = requests.delete(base_url + api_path, headers=header, data=json.dumps(body))
        response.raise_for_status()

        #event_detail = response.json()

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

    protocol = os.environ['SERVICE_EVENT_PROTOCOL']
    host = os.environ['SERVICE_EVENT_HOST']
    port = os.environ['SERVICE_EVENT_PORT']

    return protocol + '://' + host + ':' + port
