from typing import Optional
from sqlmodel import Field, SQLModel

class ItemBase(SQLModel):
    name: str
    description: Optional[str] = Field(default=None)

class Item(ItemBase, table=True):
    __tablename__: str = "items"

    id: Optional[int] = Field(primary_key=True)

class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None