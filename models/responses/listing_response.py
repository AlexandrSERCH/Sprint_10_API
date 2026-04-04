from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ListingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    name: str
    category: str
    condition: str
    city: str
    description: str
    price: int
    img1: str | None
    img2: str | None
    img3: str | None
    owner: int
    updatedAt: datetime
    createdAt: datetime
    isFavorite: bool | None


class ListingResponseError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str
    error: str
    statusCode: int
