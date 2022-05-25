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

from flask import Blueprint, render_template, request
from flask_login import login_required
from logging import getLogger

from . import get_id_token_from_session
from ..models import speaker

speaker_app = Blueprint("speaker", __name__, template_folder="templates")
logger = getLogger(__name__)

@speaker_app.route("/", methods=["GET"])
@login_required
def speaker_list():
    logger.info("call: speaker_list")

    user_info = {
        "name": "Admin",
    }

    header_data = {
        "menu_item_list": [
            {
                "name": "event list",
                "url_path": "/event",
            },
            {
                "name": "seminar list",
                "url_path": "/seminar",
            },
            {
                "name": "participant list",
                "url_path": "/participant",
            },
        ],
    }

    id_token = get_id_token_from_session()
    speakers = speaker.get_speakers(id_token)
    speakers = [
        {
            'event_path': x['speaker_id'],
            'event_name': x['speaker_name']
        } for x in speakers
    ]

    return render_template(
        "speaker/speaker.html", speakers=speakers, user_info=user_info, header_data=header_data
    )

@speaker_app.route("/<int:speaker_id>", methods=["GET"])
@login_required
def speaker_detail(speaker_id):

    logger.info("call: speaker_detail [speaker_id={}]".format(speaker_id))

    id_token = get_id_token_from_session()
    speaker_detail = speaker.get_speaker_detail(speaker_id, id_token)

    return speaker_detail

@speaker_app.route("/", methods=["POST"])
@login_required
def create_speaker():
    logger.info("call: create_speaker")

    param = request.json

    id_token = get_id_token_from_session()
    speaker.create_speaker(param, id_token)

    return '', 201

@speaker_app.route("/<int:speaker_id>", methods=["PUT"])
@login_required
def update_speaker(speaker_id):
    logger.info("call: update_speaker [speaker_id={}]".format(speaker_id))

    param = request.json

    path_speaker_id = speaker_id
    param_speaker_id = param.get('speaker_id', None)
    if is_int(param_speaker_id) and path_speaker_id != int(param_speaker_id):
        logger.info("Invalid request data: path_speaker_id={}, param_speaker_id={}".format(path_speaker_id, param_speaker_id))
        return 'invalid data.', 400

    id_token = get_id_token_from_session()
    speaker.update_speaker(param, id_token)

    return '', 204

@speaker_app.route("/<int:speaker_id>", methods=["DELETE"])
@login_required
def delete_speaker(speaker_id):
    logger.info("call: delete_speaker [speaker_id={}]".format(speaker_id))

    id_token = get_id_token_from_session()
    speaker.delete_speaker(speaker_id, id_token)

    return '', 204

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
