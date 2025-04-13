from dotenv import load_dotenv # type: ignore
from flask import Flask # type: ignore
import json
import os
import requests # type: ignore

# .envファイルを読み込む
load_dotenv()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# リフレッシュトークン取得.
@app.route('/token/auth_user')
def get_token():
    email = os.environ.get("JQUANTS_EMAIL")
    password = os.environ.get("JQUANTS_PASSWORD")
    data = {"mailaddress": email, "password": password}
    r_post = requests.post("https://api.jquants.com/v1/token/auth_user", data=json.dumps(data))
    return r_post.json()

# IDトークン取得.
@app.route('/token/auth_refresh')
def get_auth():
    refresh_token = get_token().get('refreshToken')
    r_post = requests.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={refresh_token}")
    return r_post.json()

# 上場銘柄一覧.
@app.route('/listed/info')
def get_listed_info():
    idToken = get_auth().get('idToken')
    headers = {'Authorization': 'Bearer {}'.format(idToken)}
    r = requests.get("https://api.jquants.com/v1/listed/info", headers=headers)
    return r.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)