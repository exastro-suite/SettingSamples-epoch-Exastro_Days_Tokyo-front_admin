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

import os

from flask import Blueprint, render_template, request, session
from logging import getLogger

admin_login_app = Blueprint("admin_login", __name__, template_folder="templates")
logger = getLogger(__name__)

@admin_login_app.route("/f_login", methods=["GET"])
def admin_login():
    logger.info("call: admin_login")

    sso_authc_data = {
        "google": {
            "client_id": os.environ.get('SSO_GOOGLE_CLIENT_ID', None),
        },
        "github": {
            "client_id": os.environ.get('SSO_GITHUB_CLIENT_ID', None),
        },
        "twitter": {
            "client_id": os.environ.get('SSO_TWITTER_CLIENT_ID', None),
        },
    }

    return render_template(
        "login/admin_login.html", sso_authc_data=sso_authc_data
    )

@admin_login_app.route("/logout", methods=["GET"])
def admin_logout():
    logger.info("call: admin_logout")

    session.pop('login', None)
    session.pop('user_id', None)
    session.pop('name', None)

    return '', 204
