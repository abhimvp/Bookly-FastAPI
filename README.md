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

## create Database models

- create database model for our Book Data & create read , update , delete book objects in a real persistent psql databse
- to check created tables locally :
  - psql -h localhost -U postgres
  - postgres-# \c bookly_db `to go into our database`
  - You are now connected to database "bookly_db" as user "postgres".
  - bookly_db-# \dt `to see the tables`
  - bookly_db-# \d books `to describe the tables`
  - bookly_db-# \q `to quit the interactive psql shell`
- Now we need to create service class - where we create all our CRUD operations logic - create service.py file in books directory

# Dependency Injection

- Now let's determine how we shall use our session within our path handler function & that is where concept of dependency injection comes in.
- dependency Injection is a mechanishm that FastApi uses to allow you to share logic across all route handlers that may need it.
- In our case we're having book service class having methods where each of these methods rely on a session object.
  - In case we want to go ahead & share that session object across all other methods that needed & then we need to simply pass that session to all these path handlers
  - when you're using dependency injection you're gooing to have code that's going to be relied upon by other code - so that code is what you call dependency
  - so here dependence is going to be responsible for creating our session and then we shall use that dependence see in the function that will depend on it

# Create User Authentication Model

- creating user accounts & any application requires sort of authentication (act of letting users identify who they are within our application) and authorization (allowing users to give them access to various parts of that application based on the specific roles and permissions they have)
- Here we need a way to perform migrations through our databases - as we have different models in different packages and it's not ideal to have lifespan events in every package - that's where `alembic` comes into picture - a tool that allows us to work with SQLAlchemy and orms that use sqlalchemy
- what migrations help us do is to make changes to our database without having to lose data
- let's install `alembic` - `pip install alembic`
- Now we need to create a migration environment - it helps us run our migrations inside this migration environment , we get to create versions or files that describes the changes we've been able to do on our database with time.
  - whenever we create a change to our database , we're going to create a migration and that migration is going to be reflected inside a file -> this file is going to be called version file -. inside that file we will have changes to the structure of database that we're suggesting - alemic helps migrate using templates - which provides it for using async db api
  - To create migration environment - do `alembic init -t async migrations`
  - env.py inside migrations folder is the entry point to the alemic going to be using to carry out migrations to our database
  - `alembic.ini` is the main configuration file that alembix is gng to use to do whatever it wants to our database like write our target-database we are targeting to make changes to

## configuration on migrations

- Head over to env.py in our migrations directory & import our models and point to the database that we want to target
- we do migrations as follows - `alembic revision --autogenerate -m "init"` - alembic revision - creates a version & -m means meassage
  - alembic revision --autogenerate -m "init"

````
DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/bookly_db
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected type change from VARCHAR() to Date() on 'books.published_date'
INFO  [alembic.autogenerate.compare] Detected NULL on column 'books.created_at'
INFO  [alembic.autogenerate.compare] Detected NULL on column 'books.updated_at'
Generating C:\Users\abhis\Desktop\PythonDev\Bookly-FastAPI\migrations\versions\ffd71e40a893_init.py ...  done```
````

- Above we have a version created with new users table and ignored books table as it is already present in DB provided
- Now we need migrate our changes to db - `alembic upgrade head` - looks at our latest migration and then apply to the database

```
postgres=# \c bookly_db
You are now connected to database "bookly_db" as user "postgres".
bookly_db=# \dt
              List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+----------
 public | alembic_version | table | postgres
 public | books           | table | postgres
 public | users           | table | postgres
(3 rows)
```

- `alembic_version` is what going to keep the versions of our table or versions of our migrations

# User Account Creation

Now lets build on top of User Authentical model , so users can create user accounts within our applications

- let's create routes that are responsible for our Authentication
- alembic revision --autogenerate -m "add password hash"

```
abhis@Tinku MINGW64 ~/Desktop/PythonDev/Bookly-FastAPI (main)
$ alembic revision --autogenerate -m "add password hash"
DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/bookly_db
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'users.password_hash'
INFO  [alembic.autogenerate.compare] Detected removed column 'users.password'
Generating C:\Users\abhis\Desktop\PythonDev\Bookly-FastAPI\migrations\versions\dce661513ffd_add_password_hash.py ...  done
(env)
abhis@Tinku MINGW64 ~/Desktop/PythonDev/Bookly-FastAPI (main)
$ alembic upgrade head
DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/bookly_db
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 684bd823e198 -> dce661513ffd, add password hash
(env)

```

- `pip install passlib` to deal with hashed password verification

# JWT Authentication
