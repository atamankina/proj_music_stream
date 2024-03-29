from urllib.parse import urlencode

import requests
import json

from flask import Flask
from flask import render_template
from flask import request

from gal_stream.core import read_config
# from gal_stream.core import BadRequestError
from gal_stream.auth import Authorization
from gal_stream.auth import get_auth_key


app = Flask(__name__)


@app.route("/")
def home():
    config = read_config()

    params = {
        'client_id': config.client_id,
        'response_type': 'code',
        'redirect_uri': 'http://localhost:3000/callback',
        'scope': 'user-read-private user-modify-playback-state',
    }

    enc_params = urlencode(params)
    url = f'{config.auth_url}?{enc_params}'

    return render_template('index.html', link=url)


@app.route('/callback')
def callback():
    code = request.args.get('code', '')
    response = _authorization_code_request(code)

    file = open('.gal_stream', mode='w', encoding='utf-8')
    file.write(response.refresh_token)
    file.close()

    return 'All set! You can close the browser window and stop the server.'


def _authorization_code_request(auth_code):
    config = read_config()

    auth_key = get_auth_key(config.client_id, config.client_secret)

    headers = {'Authorization': f'Basic {auth_key}', }

    options = {
        'code': auth_code,
        'redirect_uri': 'http://localhost:3000/callback',
        'grant_type': 'authorization_code',
        'json': True
    }

    response = requests.post(
        config.access_token_url,
        headers=headers,
        data=options
    )

    content = json.loads(response.content.decode('utf-8'))

    # if response.status_code == 400:
    #     error_description = content.get('error_description', '')
    #     raise BadRequestError(error_description)

    access_token = content.get('access_token', None)
    token_type = content.get('token_type', None)
    expires_in = content.get('expires_in', None)
    scope = content.get('scope', None)
    refresh_token = content.get('refresh_token', None)

    return Authorization(access_token, token_type, expires_in, scope, refresh_token)


if __name__ == '__main__':
    app.run(host='localhost', port=3000)
