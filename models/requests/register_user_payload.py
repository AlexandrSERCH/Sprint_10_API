from pydantic import BaseModel


class RegisterUserPayload(BaseModel):
    email: str
    password: str
    submitPassword: str