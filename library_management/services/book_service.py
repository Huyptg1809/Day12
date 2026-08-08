from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.book_model import BookModel
from models.author_model import AuthorModel
from schemas.book_schema import BookCreateSchema, BookUpdateSchema

def create_book(db: Session, book_in: BookCreateSchema):
    author_exists = db.query(AuthorModel).filter(AuthorModel.id == book_in.author_id).first()
    if not author_exists:
        raise HTTPException(
            status_code=400, 
            detail=f"Mã tác giả author_id = {book_in.author_id} không tồn tại trong hệ thống CSDL!"
        )
        
    db_book = BookModel(**book_in.model_dump() if hasattr(book_in, 'model_dump') else book_in.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_all_books(db: Session):
    return db.query(BookModel).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(BookModel).filter(BookModel.id == book_id).first()

def update_book(db: Session, book_id: int, book_in: BookUpdateSchema):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    
    if book_in.author_id is not None:
        author_exists = db.query(AuthorModel).filter(AuthorModel.id == book_in.author_id).first()
        if not author_exists:
            raise HTTPException(
                status_code=400, 
                detail=f"Mã tác giả author_id = {book_in.author_id} không tồn tại trong hệ thống CSDL!"
            )
    
    update_data = book_in.model_dump(exclude_unset=True) if hasattr(book_in, 'model_dump') else book_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return False
    
    db.delete(db_book)
    db.commit()
    return True
