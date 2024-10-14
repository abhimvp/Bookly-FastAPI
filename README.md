# FastAPI-Python

`ASGI` stands for `Asynchronous Server Gateway Interface`. It's a spiritual successor to WSGI (Web Server Gateway Interface), designed to improve the way Python web applications interact with web servers, especially when dealing with asynchronous operations.

### Key Concepts

- `Asynchronous Programming`: ASGI enables web applications to handle multiple requests concurrently without blocking, leading to improved performance and responsiveness, especially for I/O-bound tasks (like waiting for database queries or network responses).
- `Standard Interface:` ASGI provides a standardized way for different asynchronous web servers (like Uvicorn, Daphne) to communicate with Python web frameworks (like FastAPI, Django Channels) and applications. This promotes interoperability and flexibility.
-`Protocol Support:` While WSGI is limited to HTTP, ASGI supports both HTTP and WebSocket protocols, making it suitable for a wider range of applications, including real-time applications and chat services.

### How ASGI Works

- `Request:` When a client (e.g., a web browser) sends a request to the server, the ASGI server receives it.
- `ASGI Application:` The ASGI server passes the request to an ASGI application (your Python web application).
- `Processing:` The ASGI application processes the request asynchronously, potentially interacting with databases, external APIs, or other services.
- `Response:` Once the processing is complete, the ASGI application sends the response back to the ASGI server.
- `Client:` The ASGI server forwards the response to the client.
Benefits of ASGI

- `Performance:` Improved performance and scalability, particularly for applications with high concurrency or I/O-bound operations.
- `Flexibility:` Supports both synchronous and asynchronous applications, as well as different protocols (HTTP, WebSockets).
- `Modernization:` Enables the use of modern asynchronous features in Python (async/await).
- `Ecosystem:` Growing ecosystem of ASGI-compatible servers, frameworks, and libraries.
ASGI in FastAPI

--- `FastAPI is built on top of Starlette, which is an ASGI framework.` This means FastAPI applications are inherently ASGI-compatible and can take full advantage of asynchronous programming and the benefits of ASGI.

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
  ![alt text](images/image.png)
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

Above we built a user-authentication model and an API endpoint for creating user accounts. Now we will build on top of that to allow users identify themselves so that they can gain access to various parts of our application.

- JWt Authentication is a stateless client-side form of authentication where the users identify themselves throught the use of JWTs
- JWT stands for JSON Web Token, a standard for transmitting claims (information) among two parties
- JWTs are essentially credentials that contain information about a user(or anything)
- This information is encoded in JSON format, making it human-readable. The token is also digitally signed, ensuring it's authenticity and integrity
- A JWT contains three parts
  - A header
  - The Payload
  - The signature
- In order , these are separated by a period sign.
  ![alt text](images/image-1.png)
- How JWT Works:
  - The user logs in to the application
  - The server verifies the user's credentials
  - Upon successfull login, the server generates a JWT containing user claims.
  - For future requests, the client sends the JWT in the HTTP header.
  - The server verifies the token's signature and payload to ensure it's valid.
  - If the token is valid, the server processes the request; otheriwse, it rejects the request
- Benefits of JWTs:
  - They are compact and can be sent via URL, POST request body or headers.
  - They are self contained.
  - They are secure.
  - They can be used across different domains.
- Install pyJWt - `pip install pyjwt`
- we can create secret token as follows :

```
import secrets
>>> secrets.token_hex(16) # generates a heaxadecimal token and add this token in our .env file
```

## JWT Authentication (HTTP Bearer Auth)

Upto now we've been able to give our users access to our application by providing them with tokens. We are going to be implementing a way of limiting access to those users who do not have tokens.

- whenever a user makes a request to some protected endpoints in our API they'll need to `provide their token within an authorization header` and this is where `HTTP bearer authentication` comes in.

## JWT Authentication (creating new access tokens)

Here we will see how we can gain access tokens in case our access tokens are expired using our refresh tokens

## JWT Authentication ( Revoking User Tokens With Redis)

- Revoke Tokens on the server side
- we will make use of redis which is an in-memory data store to help us act as block list for the tokens that we shall revoke on our server side
  - scenario : Internal Server Error 500 - When we try to refresh token using expired token
- setup redis client install aioredis - which is `pip install aioredis`
  - `aioredis` is an `asynchronous Redis client` library for Python that allows you to interact with a `Redis` database using `asyncio`. It provides both low-level and high-level APIs, making it flexible for different use cases.
- If working on windows:

  - Redis is not officially supported on Windows. However, you can install Redis on Windows for development by following the instructions below.

  - To install Redis on Windows, you'll first need to enable WSL2 (Windows Subsystem for Linux). WSL2 lets you run Linux binaries natively on Windows.
  - Microsoft provides detailed instructions for [installing WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
  - start the Redis server like so: `sudo service redis-server start`
  - Instructions on installing [redis on windows](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-windows/)

```
Once Redis is running, you can test it by running redis-cli:

redis-cli
Test the connection with the ping command:

127.0.0.1:6379> ping
PONG

```

# Role Based Access Control (RBAC)

It's a mechanism that is implemented in a way that we allow access to specific endpoints or specific functionalities within our application or within our API.

- Let's implement user role and admin role and what their permissions look like below:
  ![alt text](images/image-2.png)
- After creating role in userModel - `run`

```
$ alembic revision --autogenerate -m "add roles to users"
DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/bookly_db
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'users.role'
Generating C:\Users\abhis\Desktop\PythonDev\Bookly-FastAPI\migrations\versions\0361983afabb_add_roles_to_users.py ...  done

Apply the revisions to migrate to DB: -

abhis@Tinku MINGW64 ~/Desktop/PythonDev/Bookly-FastAPI (main)
$ alembic upgrade head
DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/bookly_db
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade dce661513ffd -> 0361983afabb, add roles to users
(env)
```

To confirm changes :

```
abhis@Tinku MINGW64 ~/Desktop/PythonDev/Bookly-FastAPI (main)
$ psql -h localhost -U postgres
postgres=# \c bookly_db
You are now connected to database "bookly_db" as user "postgres".
bookly_db=# \d users
                                      Table "public.users"
 uid           | uuid                        |           | not null |
 username      | character varying           |           | not null |
 email         | character varying           |           | not null |
 firstname     | character varying           |           | not null |
 lastname      | character varying           |           | not null |
 is_verified   | boolean                     |           | not null |
 created_at    | timestamp without time zone |           |          |
 updated_at    | timestamp without time zone |           |          |
 password_hash | character varying           |           | not null |
 role          | character varying           |           | not null | 'user'::character varying
Indexes:
    "users_pkey" PRIMARY KEY, btree (uid)

```

# Model Relationships (One to Many Relationships)

- Now we need to establish relationships across the different entities that are within our application , for now we have `books` and `users` tables .
- We will also see how we can use pydantic to serialize the data in these relationships and how we can return them on our API endpoints
- Now we want to acheive an application where users will be able to submit books and those books that are submitted by them will be tracked back to them.
- That means there's going to be a relationship between users and books they submit to our application
  ![alt text](images/image-3.png)
- we're going to establish a relationship between users and books table and establish a foreign key on books table related to our user uid.Once we do that and also see how we can modify our endpoints or our responses so we can return data containing various relationships

```
alembic revision --autogenerate -m "Relate users to books"
DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/bookly_db
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'books.user_uid'
INFO  [alembic.autogenerate.compare] Detected added foreign key (user_uid)(uid) on table books
Generating C:\Users\abhis\Desktop\PythonDev\Bookly-FastAPI\migrations\versions\1e1bdbc48579_relate_users_to_books.py ...  done
(env)
alembic upgrade head
DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/bookly_db
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 0361983afabb -> 1e1bdbc48579, Relate users to books
(env)
```

## subtopic

- now let's see how relationship attributes can make it easy for us to access them using reverse relationships - what is it by the way? - it's a way we can access the user who created a certain book as well as books belong to certain user
  ![alt text](images/image-4.png)
  ![alt text](images/image-5.png)

# More Model and Schema Relationships (+ 55 min - mad stuff from Ssali)

- Link every user and every book to a review
- user will be able to submit a book review and we shall keep track of the book they made the review on and as well as the comments they made
- Every user can be able to add review to a book & we shall modify our database structure
  ![alt text](images/image-6.png)
- One user can make as many reviews as they want & also making reviews to book
- One book can have many reviews
- one to many relationship between book and reviews & user and reviews

```Let's move our models to a common module in which it will accessed throught our application

```

- Let's create reviews model

```
alembic revision --autogenerate -m "add review table"
DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/bookly_db
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'reviews'
Generating C:\Users\abhis\Desktop\PythonDev\Bookly-FastAPI\migrations\versions\0cce9b3181b2_add_review_table.py ...  done
(env)
 alembic upgrade head
DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/bookly_db
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 1e1bdbc48579 -> 0cce9b3181b2, add review table
(env)
```

- Added More routes and service methods for reviews Table
- Add Tags table and it's routes , service methods.
- All we have been looking at is creating one to many relationships and now let us look at a many to many relationship that we can set up. This is the relationship between books and tags. We want to use tags to group all books within many categories, we can also be able to search related books, basing on their tags. To begin, let us look at the structure that book tags will have.
- ![alt text](images/image-7.png)
- We've established a many-to-many relationship between books and tags, facilitated by the book_tags table. This table serves as an association table, linking instances from books to tags.
- The book_tags table functions as an intermediary or association table connecting the books and tags tables in a many-to-many relationship. It consists of two primary columns: book_id, which serves as a foreign key referencing the uid column in the books table to identify the book associated with a tag, and tag_id, a foreign key referencing the uid column in the tags table to identify the tag associated with a book

# Error Handling

- currently we are raising exceptions using HTTPException class , this is good , but there will be usecases where we want our code base to be maintainable & want to be specific about which error occurs and when it occurs - so this will be important for people who are going to maintain our code base in the future as they will know different types of errors and what they stand for & what actions can be taken
- in a case where we want to show that a token is invalid , we can create an exception class for that error so that users can be able to know the exact error that happened but also the backend user will know when to raise a specific error & at which time to raise that error
- we create a expection handler a function that fastapi will use to customize the response that's going to be returned each time we get to raise an exception

# Middle Ware

- Middleware are components (functions or classes) that lie between the requests and responses, allowing for the modification of requests before they are processed and responses before they are sent to clients.
  ![alt text](images/image-8.png)
- Each request made to the server will pass through the middleware before it is handled by the route handlers.
- Once the server has handled the request, a response is generated and still passes through the middleware before being returned to the client.

### Functions of Middleware

Using middleware, we can enhance FastAPI functionalities. Here are some of the ways we can use it:

- `Logging:` Middleware can modify how the server logs details of requests and responses for monitoring and debugging purposes.
- `Authentication:` Middleware can handle authentication by verifying if the tokens or credentials provided by clients are valid before the requests reach the application.
- `Handling CORS:` Middleware can determine which domains are allowed to access your application's resources.
- `Request Modification:` Middleware can modify requests by adding or altering headers before they reach the application.
- `Response Modification:` Middleware can modify responses by providing custom headers, changing the response body, and so on.


# Email Support 
- Sending emails is essential for user communication, identity verification, and password resets.

### FastAPI-Mail
If you've worked with Flask, you're probably familiar with Flask-Mail, the most popular extension for adding email functionality. Flask-Mail offers a simple setup for sending emails. In FastAPI, the equivalent is FastAPI-Mail, which not only provides a similar configuration process but also supports asynchronous operations and Pydantic models.
```
The code snippet includes the following imports and their purposes:

The imports

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path


FastMail: Creates the mail object, allowing access to email-sending methods.
ConnectionConfig: Sets up the email configuration for FastAPI-Mail.
MessageSchema: Structures an email before sending it.
MessageType: Specifies the type of content to send via email, such as HTML.
Config: Imports application-specific configurations, including email settings.
Path: Helps create paths, particularly for determining the location of the templates folder.
```

### User-verification 
- From the beginning, you’ll recall that we created a User authentication database model. In this model, we included an is_verified field to manage the activation of user accounts. We’ll now begin implementing the verification process using the email address provided by the user during signup.

- User account verification is crucial because it helps prevent the creation of fake accounts. Additionally, it allows us to collect user email addresses for communication and other purposes.
- To securely transfer data from our server to an untrusted environment, we will use ItsDangerous. ItsDangerous is a Python package that enables us to cryptographically sign data, ensuring that it has not been tampered with when received. The recipient can read the data but cannot modify it without access to the sender’s secret key.

- This package will be essential for creating URL-safe tokens that we will include in the user verification links sent via email.

### Adding Email Support (Password Resets)
Now that we have verified user emails, we shall proceed to allow users reset their passwords once they have forgotten them. Now the approcah for sending and decoding user details 1n the emails is the same we shall use.

test git