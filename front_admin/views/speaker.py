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

from flask import Blueprint, render_template, request, session
from flask_login import login_required
from logging import getLogger

speaker_app = Blueprint("speaker", __name__, template_folder="templates")
logger = getLogger(__name__)

@speaker_app.route("/", methods=["GET"])
@login_required
def speaker_list():
    logger.info("call: speaker_list")

    data = {}

    return render_template(
        "speaker/speaker.html", data=data
    )
