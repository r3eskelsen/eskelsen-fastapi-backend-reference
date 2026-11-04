"""Demonstration API with synthetic records; no client data."""
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./demo.db')
connect_args = {'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = 'demo_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str] = mapped_column(String(60), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

class ItemInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=60)
    quantity: int = Field(ge=0, le=1_000_000)

class ItemOutput(ItemInput):
    model_config = ConfigDict(from_attributes=True)
    id: int

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)  # demo-only; use migrations in production
    yield

app = FastAPI(title='Eskelsen Systems - Backend Reference API', version='1.0.0', lifespan=lifespan)

def get_db():
    with SessionLocal() as db:
        yield db

Db = Annotated[Session, Depends(get_db)]

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/items', response_model=ItemOutput, status_code=201)
def create_item(payload: ItemInput, db: Db):
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get('/items', response_model=list[ItemOutput])
def list_items(db: Db, limit: Annotated[int, Query(ge=1, le=100)] = 20):
    return db.scalars(select(Item).order_by(Item.id).limit(limit)).all()

@app.get('/items/{item_id}', response_model=ItemOutput)
def get_item(item_id: int, db: Db):
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@app.delete('/items/{item_id}', status_code=204)
def delete_item(item_id: int, db: Db):
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(item)
    db.commit()
