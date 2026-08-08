from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.book_schema import BookCreateSchema, BookUpdateSchema, BookResponseSchema
from services import book_service

router = APIRouter(prefix="/api/v1/books", tags=["Book Controller"])

@router.post("", response_model=BookResponseSchema, status_code=201)
def create_book(book_in: BookCreateSchema, db: Session = Depends(get_db)):
    """Tạo mới một cuốn sách vào CSDL."""
    return book_service.create_book(db, book_in)

@router.get("", response_model=List[BookResponseSchema])
def get_books(db: Session = Depends(get_db)):
    """Lấy danh sách toàn bộ sách."""
    return book_service.get_all_books(db)

@router.get("/{id}", response_model=BookResponseSchema)
def get_book(id: int, db: Session = Depends(get_db)):
    """Xem chi tiết một cuốn sách theo ID."""
    db_book = book_service.get_book_by_id(db, id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Sách không tồn tại trong hệ thống")
    return db_book

@router.put("/{id}", response_model=BookResponseSchema)
def update_book(id: int, book_in: BookUpdateSchema, db: Session = Depends(get_db)):
    """Cập nhật thông tin cuốn sách theo ID."""
    updated_book = book_service.update_book(db, id, book_in)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Sách không tồn tại trong hệ thống")
    return updated_book

@router.delete("/{id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    """Xóa cuốn sách khỏi CSDL theo ID."""
    is_deleted = book_service.delete_book(db, id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Sách không tồn tại trong hệ thống")
    return {"message": f"Đã xóa thành công sách ID {id}"}
