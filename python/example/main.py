from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Friend(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    city: str
    country: str
    phone: str


sqlite_file_name = "friends.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    pass


app = FastAPI(lifespan=lifespan)


@app.post("/friends/", response_model=Friend)
def create_friend(friend: Friend):
    with Session(engine) as session:
        session.add(friend)
        session.commit()
        session.refresh(friend)
        return friend


@app.get("/friends/", response_model=List[Friend])
def read_friends():
    with Session(engine) as session:
        friends = session.exec(select(Friend)).all()
        return friends


@app.get("/friends/{friend_id}", response_model=Friend)
def read_friend(friend_id: int):
    with Session(engine) as session:
        friend = session.get(Friend, friend_id)
        if not friend:
            raise HTTPException(status_code=404, detail="Friend not found")
        return friend


@app.put("/friends/{friend_id}", response_model=Friend)
def update_friend(friend_id: int, friend: Friend):
    with Session(engine) as session:
        db_friend = session.get(Friend, friend_id)
        if not db_friend:
            raise HTTPException(status_code=404, detail="Friend not found")
        db_friend.name = friend.name
        db_friend.city = friend.city
        db_friend.country = friend.country
        db_friend.phone = friend.phone
        session.add(db_friend)
        session.commit()
        session.refresh(db_friend)
        return db_friend


@app.delete("/friends/{friend_id}")
def delete_friend(friend_id: int):
    with Session(engine) as session:
        friend = session.get(Friend, friend_id)
        if not friend:
            raise HTTPException(status_code=404, detail="Friend not found")
        session.delete(friend)
        session.commit()
        return {"message": "Friend deleted successfully"}


@app.get("/")
def index():
    return {"message": "Hello world!"}
