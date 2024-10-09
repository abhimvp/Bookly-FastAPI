# contains API endpoints that are going to be specific to our books
# here we create our Fast API router - A Router Object - Similar to fast APi instance in main.py - from fastapi import APIRouter
from typing import  List
from fastapi import APIRouter, HTTPException, status
from src.books.schemas import Book, BookUpdateModel
from src.books.book_data import books


book_router = APIRouter()

@book_router.get('/' , response_model=List[Book])
async def get_all_books():
    return books

@book_router.post('/',status_code=status.HTTP_201_CREATED)
async def create_a_books(book_data: Book):
    new_book = book_data.model_dump() # Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
    books.append(new_book)
    return new_book

# try to retruve single book from our data store
@book_router.get('/{book_id}')
async def get_book_by_id(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch('/{book_id}')
async def update_book(book_id: int, book_update_data: BookUpdateModel):
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update_data.title
            book["author"] = book_update_data.author
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language

            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") 

@book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """_summary_

    Args:
        book_id (int): _description_

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")