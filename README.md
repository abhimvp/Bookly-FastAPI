# FastAPI-Python

### Learning from [Ssali Jonathan YT](https://youtu.be/TO4aQ3ghFOc?si=NYiKd6YoKTRwwiaf) FastAPI Beyond CRUD Full Course

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

# CRUD API

https://jod35.github.io/fastapi-beyond-crud-docs/site/
Build a REST API on a Python List - let's consider it as inmemory database

# A better file structure with Routers

- It's a good idea to structure our project that is going to grow as our project grows - This is where the `FastAPI routers` comes into picture.
- Fast API routers allow us to make our application modular by splitting our API endpoints into modules or grouping them into modules on which you can access them using a specific prefix
- we will be doing that by creating an object that is similar to our app instance - within that object we can be able to group API endpoints that are related together & we can put them in their own seperate module
  ![alt text](image.png)
- `pip freeze > requirements.txt` - to load the requirements for this application in future as well with same requirements

# Databases with SQLModel

Let's make our application adapt to a persistant database

- FastAPI supports various types of databases,including relational/SQL databases and non-relational/NoSQL databases.
- This project we'll focus on using a relational database, specifically PostgreSQL
- while using PostgreSQL, we shall need to choose a way to interact with database using the python language. That introduces us to the concept of Object Relational mapper (ORM)
- An Object Relational mapper (ORM) translates between a programming language such as python and a database like PostgreSQL
- Mapping Objects to Tables:
  - You create python classes to represent tables in the database. Each object of these classes corresponds to a row in the database tables
  - Interacting with data : You can then interact with these python objects as if they were regular objects in your code , like setting attributes and calling methods.
  - Behind the Scenes : When you perform operations on these objects , like saving or deleting , the ORM translates these actions into the appropriate SQL queries that the database understands.
  - Data Conversion : The ORM handles converting Python data types into database-specific types and vice-versa, ensuring compatability between the two.
  - `SQLAlchemy` is the most popular ORM for python, mapping objects to database tables and providing a high-level SQL language
  - While SQLAlchemy is powerful, `SQLModel` offers a seamless integration with SQLAlchemy and pydantic. SQLModel, designed for use with FastAPI , was developed by the creator of FastAPI. This project explores using SQLModel
  - An ORM simplifies database interactions by letting developers use Python instead of SQL
- connect with PostgreSQL locally `psql -h localhost -U postgres`
- do the following in the psql interactive shell
  - CREATE DATABASE bookly_db;
  - Now for us to formulate the url to this PostgreSQL database , we create `.env` file in the books package - where we include all the settings for our project , these wouldn't be included in Version control
  - then we will use a `ASYNC DB API` - where python allows us to access db - for that need to install - `pip install asyncpg`
    - create env variable DATBASE_URL = postgres+asyncpg://username:password@localhost:port/DATABASE_NAME
  - then we install - `pip install pydantic-settings` - to read our env variable in our application - create `config.py` in books package
  - After building our pydantic model , let's install sqlmodel -`pip install sqlmodel` & also create `db` package in `src` directory
