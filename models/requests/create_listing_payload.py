from enum import Enum

from pydantic import BaseModel


class ListingCategory(str, Enum):
    AUTO = "Авто"
    BOOKS = "Книги"
    GARDENING = "Садоводство"
    HOBBY = "Хобби"
    TECHNOLOGY = "Технологии"


class ListingCondition(str, Enum):
    NEW = "Новый"
    USED = "Б/У"


class CreateListingPayload(BaseModel):
    name: str
    category: ListingCategory
    condition: ListingCondition
    city: str
    description: str
    price: int
