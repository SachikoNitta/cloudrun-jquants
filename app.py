from dotenv import load_dotenv # type: ignore
from flask import Flask # type: ignore
import json
import os
import requests # type: ignore
from google.cloud import firestore # type: ignore
from firestore_utils import initialize_firestore_client, save_to_firestore, test_firestore_connection

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
    data = r.json()

    return data

# 上場銘柄一覧をFirestoreに保存.
@app.route('/listed/info/store')
def save_listed_info():
    # 上場銘柄一覧を取得
    listed_info = get_listed_info()

    # Firestore に保存
    save_to_firestore("listed_info", listed_info)

    return {"message": "Listed info saved to Firestore."}

# FireStoreに接続できてるかテスト.
@app.route('/firestore/test')
def test_firestore_connection_route():
    try:
        return test_firestore_connection()
    except Exception as e:
        return {"message": "Firestore connection failed.", "error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)