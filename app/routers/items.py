from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.db.handlers.items_handler import ItemHandler
from app.models.item import Item, ItemUpdate, ItemCreate


router = APIRouter(
    prefix="/items",
)


@router.post("/", response_model=Item)
def create(
    item: ItemCreate, db_session: Session = Depends(get_db)
) -> Item:
    item_handler = ItemHandler(db_session)
    return item_handler.create(item)


@router.get("/{item_id}", response_model=Item)
def get(item_id: int, db_session: Session = Depends(get_db)) -> Item:
    item_handler = ItemHandler(db_session)
    item = item_handler.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=Item)
def update(
    item_id: int, item: ItemUpdate, db_session: Session = Depends(get_db)
) -> Item:
    item_handler = ItemHandler(db_session)
    return item_handler.update(item_id, item)


@router.delete("/{item_id}", response_model=Item)
def delete_item(item_id: int, db_session: Session = Depends(get_db)) -> Item:
    item_handler = ItemHandler(db_session)
    return item_handler.delete(item_id)
