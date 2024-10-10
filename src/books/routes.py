# contains API endpoints that are going to be specific to our books
# here we create our Fast API router - A Router Object - Similar to fast APi instance in main.py - from fastapi import APIRouter
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from src.books.service import BookService

# from src.books.book_data import books
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer


book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()


@book_router.get("/", response_model=List[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    print(user_details)
    # {'user': {'email': 'abhimvpuser@gmail.com', 'user_uid': '47d41d27-6a15-4889-9e10-233656724c0e'}, 'exp': 1728562046.135454, 'jti': 'daddfc82-7ee6-448c-99bc-e668b12e0b69', 'refresh': False}
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_books(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    # new_book = book_data.model_dump() # Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
    # books.append(new_book)
    new_book = await book_service.create_book(book_data, session)
    return new_book


# try to retruve single book from our data store
@book_router.get("/{book_uid}", response_model=Book)
async def get_book_by_id(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.patch("/{book_uid}")
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    deleted_book = await book_service.delete_book(book_uid, session)
    if deleted_book:
        return None
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
