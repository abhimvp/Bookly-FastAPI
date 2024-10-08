# let's create an instance of fast api application - every application have main app instance that's is going to be entry point to our fastAPI application
from fastapi import FastAPI ,Header
from typing import Optional
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