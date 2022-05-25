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

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, login_required
from logging import getLogger

from ..models.auth import User

admin_login_app = Blueprint("admin_login", __name__, template_folder="templates")
logger = getLogger(__name__)


@admin_login_app.route("/login_b", methods=['GET', 'POST'])
def admin_basic_login():
    logger.info("call: admin_basic_login")

    if request.method == 'GET':
        return render_template('login/admin_login.html', login_path="/login_b")

    form_username = request.form.get('username', 'guest')
    form_password = request.form.get('password', '')
    remember = True if request.form.get('remember', False) else False

    # workaround
    user_auth_data = {
        'username': 'admin', # os.environ['ADMIN_NAME'],
        'password': 'password' # os.environ['ADMIN_PASSWORD'],
    }

    #if check_password_hash(user.password, password):
    if user_auth_data['username'] == form_username and user_auth_data['password'] == form_password:
        user = User()
        login_user(user, remember=remember)
        return redirect(url_for('event.event_list'))
    else:
        return redirect(url_for('admin_login.admin_basic_login'))

@admin_login_app.route("/login_o", methods=['GET', 'POST'])
def admin_oidc_login():
    logger.info("call: admin_oidc_login")

    if request.method == 'GET':
        return render_template('login/admin_login.html', login_path="/login_o")

    form_username = request.form.get('username', 'guest')
    form_password = request.form.get('password', '')
    remember = True if request.form.get('remember', False) else False

    # workaround
    id_token = get_id_token(form_username, form_password)

    #if check_password_hash(user.password, password):
    if id_token:
        user = User()
        login_user(user, remember=remember)
        
        session['login'] = True
        session['id_token'] = id_token

        return redirect(url_for('event.event_list'))
    else:
        return redirect(url_for('admin_login.admin_oidc_login'))

def get_id_token(username, password):

    # $ curl http://xxx.xxx.xx.xx:yyyyy/realms/bookinfo/protocol/openid-connect/token
    #    -d "grant_type=password&username=sample_user&password=<password>&client_id=sample_application&client_secret=<client secret>&scope=openid"

    protocol = os.environ['OIDC_SERVER_PROTOCOL']
    host = os.environ['OIDC_SERVER_HOST']
    port = os.environ['OIDC_SERVER_PORT']
    realm = os.environ['OIDC_REALM']
    client_id = os.environ['OIDC_CLIENT_ID']
    client_secret = os.environ['OIDC_CLIENT_SECRET']

    base_url = protocol + '://' + host + ':' + port
    api_path = '/realms/{}/protocol/openid-connect/token'.format(realm)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    body_str = 'scope=openid' + \
        '&grant_type=password' + \
        '&username={}'.format(username) + \
        '&password={}'.format(password) + \
        '&client_id={}'.format(client_id) + \
        '&client_secret={}'.format(client_secret)

    try:
        # 取得
        logger.debug("request_url: {}".format(base_url + api_path))
        # logger.debug("request_body: {}".format(json.dumps(body)))
        # logger.debug("request_body: {}".format(body_str))
        response = requests.post(base_url + api_path, headers=headers, data=body_str)
        response.raise_for_status()

        return response.json()['id_token']

    except Exception as e:
        logger.debug(e)
        logger.debug("traceback:" + traceback.format_exc())

        return None

@admin_login_app.route("/logout", methods=["GET"])
@login_required
def admin_logout():
    logger.info("call: admin_logout")

    logout_user()

    session.pop('login', None)
    session.pop('id_token', None)

    return '', 204
