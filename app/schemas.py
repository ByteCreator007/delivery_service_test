from pydantic import BaseModel, Field
from typing import Optional

# Схема для создания посылки
class PackageCreate(BaseModel):
    name: str = Field(..., example="Ноутбук")
    weight: float = Field(..., gt=0, example=2.5)
    type_id: int = Field(..., example=2)  # id типа из таблицы package_types
    content_value: float = Field(..., gt=0, example=1500.0)

# Схема для ответа с данными посылки
class PackageResponse(BaseModel):
    id: int
    name: str
    weight: float
    type_name: str
    content_value: float
    shipping_cost: Optional[str] = Field(None, description="Если доставка не рассчитана, вернуть 'Не рассчитано'")

    class Config:
        from_attributes = True

# Схема для типа посылки
class PackageTypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
