from pydantic import BaseModel, ConfigDict


class UserItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    name: str
    email: str


class AccessTokenItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str


class RegisterUserResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user: UserItem
    access_token: AccessTokenItem
