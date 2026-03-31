from pydantic import BaseModel, ConfigDict


class UserItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    name: str
    email: str
    avatar: str | None
    admin: bool


class AccessTokenItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str


class AuthUserResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user: UserItem
    token: AccessTokenItem
