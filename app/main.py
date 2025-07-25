from fastapi import FastAPI, HTTPException, Request
from .schemas import *
from .crypto_utils import encrypt_b64, decrypt_to_b64
from .db import save_secret, get_secret

app = FastAPI(title="Secret Manager")

@app.post("/vault/secret/create/", response_model=CreateSecretResp)
def create_secret(req: CreateSecretReq):
    try:
        cipher = encrypt_b64(req.secret)
        sid = save_secret(cipher.encode())   # 存 bytes
        return {"secret_id": sid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/vault/secret/fetch", response_model=FetchSecretResp)
def fetch_secret(req: FetchSecretReq):
    cipher = get_secret(req.secret_id)
    if cipher is None:
        raise HTTPException(status_code=404, detail="Secret not found")
    try:
        plain_b64 = decrypt_to_b64(cipher.decode())
        return {"secret": plain_b64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))