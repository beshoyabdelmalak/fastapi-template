from fastapi.testclient import TestClient
from sqlmodel import Session
from app.db.handlers.items_handler import ItemHandler
from app.models.item import Item, ItemCreate, ItemUpdate

def test_create_item(client: TestClient):
    item = ItemCreate(name="test item", description="test description")
    response = client.post("/items/", json=item.model_dump())
    assert response.status_code == 200
    data = response.json()
    created_item = Item(**data)
    assert created_item.name == item.name
    assert created_item.description == item.description

def test_get_item_non_existent(client: TestClient):
    response = client.get("/items/1")
    assert response.status_code == 404

def test_get_item(client: TestClient, db_session: Session):
    item_handler = ItemHandler(db_session)
    item = ItemCreate(name="test item", description="test description")
    created_item = item_handler.create(item)

    response = client.get(f"/items/{created_item.id}")
    assert response.status_code == 200
    data = response.json()
    item = Item(**data)
    assert item.name == created_item.name
    assert item.description == created_item.description

def test_update_item_non_existent(client: TestClient):
    item = ItemUpdate(name="test item")

    response = client.put("/items/1", json=item.model_dump())
    assert response.status_code == 404


def test_update_item(client: TestClient, db_session: Session):
    item_handler = ItemHandler(db_session)
    item = ItemCreate(name="test item", description="test description")
    created_item = item_handler.create(item)

    item = ItemUpdate(name="test item")

    response = client.put(f"/items/{created_item.id}", json=item.model_dump())
    assert response.status_code == 200
    data = response.json()
    updated_item = Item(**data)
    assert updated_item.name == item.name
    assert updated_item.description == created_item.description


def test_delete_item_non_existent(client: TestClient):
    response = client.delete("/items/1")
    assert response.status_code == 404


def test_delete_item(client: TestClient, db_session: Session):
    item_handler = ItemHandler(db_session)
    item = ItemCreate(name="test item", description="test description")
    created_item = item_handler.create(item)

    response = client.delete(f"/items/{created_item.id}")
    assert response.status_code == 200
    data = response.json()
    updated_item = Item(**data)
    assert updated_item.name == item.name
    assert updated_item.description == created_item.description


