import uuid, datetime
from pymongo import MongoClient
from .config import MONGO_URI

client = MongoClient(MONGO_URI)
db  = client["vault"]
col = db["secrets"]

def save_secret(ciphertext: bytes) -> str:
    sid = str(uuid.uuid4())
    col.insert_one({"_id": sid,
                    "ciphertext": ciphertext,
                    "created_at": datetime.datetime.utcnow()})
    return sid

def get_secret(sid: str) -> bytes | None:
    doc = col.find_one({"_id": sid}, {"ciphertext": 1})
    return doc["ciphertext"] if doc else None