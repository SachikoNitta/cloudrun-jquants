# firestore_utils.py
from google.cloud import firestore
import os

def initialize_firestore_client():
    return firestore.Client(database=get_firestore_db_name())

def get_firestore_db_name():
    db_name = os.environ.get("FIRESTORE_DB_NAME")
    if not db_name:
        raise ValueError("Firestore DB name is not set in environment variables.")
    return db_name

def test_firestore_connection():
    firestore_client = initialize_firestore_client().collection("test")
    doc_ref = firestore_client.document("ping")

    # 適当なデータを書き込む
    doc_ref.set({
        "message": "pong",
    })

    # データを読み込む
    doc = doc_ref.get().to_dict()
    return {
        "message": "Firestore connection successful.",
        "Data": doc
      }, 200

def save_to_firestore(collection_name, data):
    firestore_client = initialize_firestore_client().collection(collection_name)
    if data and 'info' in data:
        info_data = data['info']
        for item in info_data:
            doc_ref = firestore_client.document()
            doc_ref.set(item)

