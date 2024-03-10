from dataclasses import dataclass
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from requests import Session as RequestsSession

from app.models.item import Item, ItemUpdate, ItemCreate


@dataclass
class ItemHandler:
    db_session: Session

    def create(self, create_item: ItemCreate) -> Item:
        item = Item(**create_item.model_dump())
        self.db_session.add(item)
        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def get_by_id(self, item_id: int) -> Optional[Item]:
        return self.db_session.query(Item).filter(
            Item.id == item_id
        ).first()


    def update(self, item_id: int, item: ItemUpdate) -> Item:
        db_item = self.get_by_id(item_id)
        if db_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        for key, value in item.model_dump(exclude_none=True).items():
            setattr(db_item, key, value)

        self.db_session.commit()
        self.db_session.refresh(db_item)
        return db_item


    def delete(self, item_id: int) -> Item:
        db_item = self.get_by_id(item_id)
        if db_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item not found"
            )
        self.db_session.delete(db_item)
        self.db_session.commit()
        return db_item
