from pydantic import BaseModel


class AuthUserPayload(BaseModel):
    email: str
    password: str
