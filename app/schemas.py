from pydantic import BaseModel, Field

class CreateSecretReq(BaseModel):
    secret: str = Field(..., description="Base64 plaintext")

class CreateSecretResp(BaseModel):
    secret_id: str

class FetchSecretReq(BaseModel):
    secret_id: str

class FetchSecretResp(BaseModel):
    secret: str