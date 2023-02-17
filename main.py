
from fastapi import FastAPI,  Request
import databases
import sqlalchemy

import uvicorn

DATABASE_URL = "postgresql://postgres:postgre@localhost:5432/posgres"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()



app = FastAPI()


books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column('author', sqlalchemy.String),
    # sqlalchemy.Column('reader_id', sqlalchemy.ForeignKey("readers.id"), nullable=False,index=True),
    )

readers = sqlalchemy.Table(
    "readers",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    )

readers_books = sqlalchemy.Table(
    "readers_books",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("books_id", sqlalchemy.ForeignKey("books.id")),
    sqlalchemy.Column("readers_id", sqlalchemy.ForeignKey("readers.id"))
    )
                  
@app.on_event("startup")
async def startup():
    await database.connect()
    
    
    
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    

@app.get("/books") 
async def get_books():
    query = books.select()      
    return await database.fetch_all(query) 


@app.post("/create-books/")
async def create_books(request : Request):
    data = await request.json()
    query = books.insert().values(**data)
    last_record_id = await database.execute(query)
    return {"id" :last_record_id}

@app.post("/create-readers/")
async def create_reders(request : Request):
    data = await request.json()
    query = readers.insert().values(**data)
    last_record_id = await database.execute(query)
    return {"id" :last_record_id}

@app.post("/read/")
async def create_reders(request : Request):
    data = await request.json()
    query = readers_books.insert().values(**data)
    last_record_id = await database.execute(query)
    return {"id" :last_record_id}

if __name__ == "__main__":
    uvicorn.run("main:app")
