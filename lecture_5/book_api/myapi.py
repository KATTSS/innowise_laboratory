# Import libraries and packages
from fastapi import FastAPI, HTTPException, status, Path, Depends
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI(title="My Book API")

# Database setup
engine=create_engine("sqlite:///book.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)

Base.metadata.create_all(engine)

# Pydantic models (Dataclass)
class BookCreate(BaseModel):
    title:str
    author:str
    year:int

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int

    class Config:
        from_attributes=True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint (URL)
@app.get("/")
def root():
    return {"message":"Welcome to my Book API"}

# Get all books
@app.get("/books/", response_model=List[BookResponse])
def get_book(db: Session = Depends(get_db)):
    books=db.query(Book).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

# Create book
@app.post("/books/",response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db:Session = Depends(get_db)):
    if db.query(Book).filter(Book.title == book.title).first():
        raise HTTPException(status_code=400, detail="Book already exists")

    new_book=Book(
        title=book.title,
        author=book.author,
        year=book.year
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# Update book
@app.put("/books/{id}")
def update_book(id:int, book:BookCreate, db:Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not exists")
    for field, value in book.model_dump().items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)

# Delete book
@app.delete("/books/{id}")
def delete_book(id:int, db:Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not exists")
    db.delete(db_book)
    db.commit()

# Search for a book
@app.get("/books/search/", response_model=List[BookResponse])
def search_book(title: Optional[str]=None, author:Optional[str]=None, year:Optional[int]=None, db:Session = Depends(get_db)):
    db_book = db.query(Book)
    if title:
        db_book = db_book.filter(Book.title.ilike(f"%{title}%"))
    if author:
        db_book = db_book.filter(Book.author.ilike(f"%{author}%"))
    if year:
        db_book = db_book.filter(Book.year == year)

    db_book = db_book.all()
    if not db_book or (not title and not author and not year):
        raise HTTPException(status_code=404, detail="Book not exists")
    return db_book
