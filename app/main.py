from fastapi import FastAPI, HTTPException, Request
from .schemas import *
from .crypto_utils import encrypt_b64, decrypt_to_b64
from .db import save_secret, get_secret
import base64, binascii
from fastapi import HTTPException


app = FastAPI(title="Secret Manager")

def _validate_b64(s: str) -> None:
    try:
        base64.b64decode(s, validate=True)
    except binascii.Error as e:
        raise HTTPException(status_code=400, detail=f"invalid base64: {e}")
    

@app.post("/vault/secret/create/", response_model=CreateSecretResp)
def create_secret(req: CreateSecretReq):
    _validate_b64(req.secret)
    try:
        cipher_b64 = encrypt_b64(req.secret)  # encrypt base64
        sid = save_secret(cipher_b64)  # save ciphertext_b64
        return {"secret_id": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vault/secret/fetch", response_model=FetchSecretResp)
def fetch_secret(req: FetchSecretReq):
    cipher_b64 = get_secret(req.secret_id)
    if cipher_b64 is None:
        raise HTTPException(status_code=404, detail="Secret not found")
    try:
        plain_b64 = decrypt_to_b64(cipher_b64)
        return {"secret": plain_b64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))