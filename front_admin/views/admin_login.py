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

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from logging import getLogger

from ..models.auth import User

admin_login_app = Blueprint("admin_login", __name__, template_folder="templates")
logger = getLogger(__name__)


@admin_login_app.route("/login", methods=['GET', 'POST'])
def admin_login():
    logger.info("call: admin_login")

    if request.method == 'GET':
        return render_template('login/admin_login.html')

    else:
        username = request.form.get('username', 'guest')
        password = request.form.get('password', '')
        remember = True if request.form.get('remember', False) else False

        # workaround
        user = {
            'username': 'admin', # os.environ['ADMIN_NAME'],
            'password': 'password' # os.environ['ADMIN_PASSWORD'],
        }

        #if check_password_hash(user.password, password):
        if user['username'] == username and user['password'] == password:
            user = User()
            login_user(user, remember=remember)
            return redirect(url_for('event.event_list'))
        else:
            return redirect(url_for('admin_login.admin_login'))

@admin_login_app.route("/logout", methods=["GET"])
@login_required
def admin_logout():
    logger.info("call: admin_logout")

    logout_user()

    return '', 204
