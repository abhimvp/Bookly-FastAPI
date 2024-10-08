# let's create an instance of fast api application - every application have main app instance that's is going to be entry point to our fastAPI application
from fastapi import FastAPI ,Header , status
from fastapi.exceptions import HTTPException
from typing import Optional , List
from pydantic import BaseModel
from fastapi import Depends


app = FastAPI() # this is going to be our FASTAPI Instance or object , with this app , we can pretty much get access
#  to create middleware , to create routes , to access HTTP methods  and to create request and response bodies , which are going to be present within this app variable

#let's create fast api endpoint or path
@app.get("/") # this is going to be our root path or endpoint -  http://127.0.0.1:8000/
async def read_root(): # async function is called as routine & this fucntion will be called when we call that endpoint
    return {"message": "Hello World"}

@app.get("/greet/{name}") # here {name} is a path parameter which is dynamic you may pass in our url - a way to send data to our server - #  http://127.0.0.1:8000/greet/abhimvp
async def greet_name(name: str):
    return {"message": f"Hello {name}"}

@app.get("/greetqp") # query parameter is a way to send data to our server through url - # http://127.0.0.1:8000/greetqp?name=abhimvp
async def query_parameter(name: str):
    return {"message": f"Hello {name}"}

# How we can use path parameter and query parameter together
@app.get("/greetq&p/{name}") # query parameter is a way to send data to our server through url - #  http://127.0.0.1:8000/greetq&p/abhimvp?age=26
async def query_path_parameter(name: str, age: int):
    return {"message": f"Hello {name}, you are {age} years old"}

# query parameters optional or not
@app.get("/greetq&p2") # query parameter is a way to send data to our server through url - #  http://127.0.0.1:8000/greetq&p2?name=abhi&age=26
async def query_path_parameter_optional(name: Optional[str] = "User", age: int = 0 ):
    return {"message": f"Hello {name}, you are {age} years old"}

# send data to our server using a request body to validate or create resources
# one thing we need to understand is when making a post request or any sort of request that involves sending data to the server
#  then we need a way to validate this data - so to validate the data we're going to create what is a serialization model
# serialization model is one that's  going to help us change data from the database or change data from our server into something 
# that any client that makes a request to our server can understand & it can also be reverse - where we get data from a client
# we need to install pydantic - pip install pydantic

# this class defines the data or the fields of the data - that we want to send from our client to our server & vice versa
class BookCreateModel(BaseModel):
    title: str
    author: str
    # year: int
    # genre: str

@app.post('/create_book') # post is  used to send and update data to our server
async def create_book(book_data:BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author 
    }

# get -headers
@app.get('/get_headers',status_code=201)
async def get_headers(
    accept:str =  Header(None),
    content_type: str =Header(None),
    user_agent: str = Header(None),
    host: str = Header(None)
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host
    return request_headers

## CRUD API

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

books = [
    {
        "id": 1,
        "title": "Think Python",
        "author": "Allen B. Downey",
        "publisher": "O'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Django By Example",
        "author": "Antonio Mele",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2022-01-19",
        "page_count": 1023,
        "language": "English",
    },
    {
        "id": 3,
        "title": "The web socket handbook",
        "author": "Alex Diaconu",
        "publisher": "Xinyu Wang",
        "published_date": "2021-01-01",
        "page_count": 3677,
        "language": "English",
    },
    {
        "id": 4,
        "title": "Head first Javascript",
        "author": "Hellen Smith",
        "publisher": "Oreilly Media",
        "published_date": "2021-01-01",
        "page_count": 540,
        "language": "English",
    },
    {
        "id": 5,
        "title": "Algorithms and Data Structures In Python",
        "author": "Kent Lee",
        "publisher": "Springer, Inc",
        "published_date": "2021-01-01",
        "page_count": 9282,
        "language": "English",
    },
    {
        "id": 6,
        "title": "Head First HTML5 Programming",
        "author": "Eric T Freeman",
        "publisher": "O'Reilly Media",
        "published_date": "2011-21-01",
        "page_count": 3006,
        "language": "English",
    },
]

@app.get('/books' , response_model=List[Book])
async def get_all_books():
    return books

@app.post('/books',status_code=status.HTTP_201_CREATED)
async def create_a_books(book_data: Book):
    new_book = book_data.model_dump() # Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
    books.append(new_book)
    return new_book

# try to retruve single book from our data store
@app.get('/book/{book_id}')
async def get_book_by_id(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.patch('/book/{book_id}')
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

@app.delete('/book/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")