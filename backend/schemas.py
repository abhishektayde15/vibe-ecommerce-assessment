from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    rating: int
    image: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Headphones",
                "category": "Electronics",
                "price": 299.99,
                "rating": 5,
                "image": "http://example.com/img.png"
            }
        }
