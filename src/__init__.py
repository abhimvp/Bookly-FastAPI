# This __init__.py file is going to mark this src folder as a python package

# from now on we're going to access everything inside source folder 
# so we will be writing all of our app logic inside the  __init__.py 
# so our main entry point for this project is going to be our source folder

from fastapi import FastAPI
from src.books.routes import book_router

VERSION = "v1"

app = FastAPI(
    title= "Bookly API",
    description= "A REST API for a book review web service",
    version= VERSION,
)
# now this app instance can also be used to provide api version info

app.include_router(book_router, prefix=f"/api/{VERSION}/books",tags=['books'])
# prefix is used to define on which endpoint we're going to access all the endpoints that are related to our books 

# fastapi dev src/ - this is how we tell fastapi that our src directory is the main entry point of our application
# It will scan for the app instance - which it will find it within our src/__init__.py 