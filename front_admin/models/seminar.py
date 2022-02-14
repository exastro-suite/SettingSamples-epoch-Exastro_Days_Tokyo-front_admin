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


def _create_header():
    # ヘッダ情報
    header = {
        'Content-Type': 'application/json',
    }

    return header

def _create_base_url():

    protocol = os.environ['SERVICE_EVENT_PROTOCOL']
    host = os.environ['SERVICE_EVENT_HOST']
    port = os.environ['SERVICE_EVENT_PORT']

    return protocol + '://' + host + ':' + port
