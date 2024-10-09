# FastAPI-Python - 1st commit

### Learning from ![Ssali Jonathan YT](https://youtu.be/TO4aQ3ghFOc?si=NYiKd6YoKTRwwiaf) FastAPI Beyond CRUD Full Course

_ How do we build web applications using FastAPI - a web framework for building web applications using python.
_ It gives us the ability to allow to build something performant while also being simple and helpful

- create virtual environment - `python -m venv env` & activate it - `source env/scripts/activate`.
- Installing Fast API - `pip install fastapi` - which will add fastapi into our virtual environment.

\_\_ Now let's create a simple web server - in `main.py` file

- to use FAST_API CLI eg: `fastapi --help` - install - `pip install "fastapi[standard]"`
- we will make use of `https://restfox.dev/` as a client similar to how we use postman to make requests to our server
- FastAPi relies on pydantic - a data validation tool - that helps us to easily validate the kind of data we pass through to our API
  Covered the following:
  Introduction  
  (0:01:00) Project setup  
  (0:07:30) Build a simple web server  
  (0:10:45) Run the server with FastAPI CLI  
  (0:14:11) Path parameters  
  (0:17:23) Choosing an HTTP client  
  (0:20:58) Query parameters  
  (0:24:40) Using Path and Query parameters  
  (0:26:51) Optional Query parameters  
  (0:31:48) Request Body  
  (0:39:11) Reading and setting headers

# CRUD API - commit 2

https://jod35.github.io/fastapi-beyond-crud-docs/site/
Build a REST API on a Python List - let's consider it as inmemory database

# A better file structure with Routers - commit 3

- It's a good idea to structure our project that is going to grow as our project grows - This is where the `FastAPI routers` comes into picture.
- Fast API routers allow us to make our application modular by splitting our API endpoints into modules or grouping them into modules on which you can access them using a specific prefix
- we will be doing that by creating an object that is similar to our app instance - within that object we can be able to group API endpoints that are related together & we can put them in their own seperate module
  ![alt text](image.png)
- `pip freeze > requirements.txt` - to load the requirements for this application in future as well with same requirements
