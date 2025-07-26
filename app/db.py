import uuid, datetime
from pymongo import MongoClient
from .config import MONGO_URI
from uuid import UUID
from typing import Union

client = MongoClient(MONGO_URI)
db  = client["vault"]
col = db["secrets"]

def save_secret(ciphertext_b64: str) -> str:
    sid = str(uuid.uuid4())
    col.insert_one({"_id": sid,
                    "ciphertext": ciphertext_b64, 
                    "created_at": datetime.datetime.utcnow()})
    return sid

def get_secret(sid: Union[str, UUID]) -> str | None:
    if isinstance(sid, UUID):
        sid = str(sid) 
    doc = col.find_one({"_id": sid}, {"ciphertext": 1})
    return doc["ciphertext"] if doc else None