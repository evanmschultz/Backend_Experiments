from enum import Enum
from fastapi import FastAPI

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


"""
Path parameters with typing
"""


# @app.get("/items/{item_id}")
# async def read_item_prime(item_id: int):
#     return {"item_id": item_id}


"""
Paths are read in order, so place fixed paths before variable paths.
If not done this way the path would be interpreted as "/users/{user_id} = "me"
instead of "/users/me".
"""


# @app.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the current user"}


# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id}


"""
Enum (enumeration) example:
Enums allow you to define a set of symbolic names bound to unique, constant values, 
instead of vague generic types, ie. str.
"""


# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"


# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     # Compare arg with the literal enumeration member
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     # Compare arg value with member value
#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}


"""
Path parameters {file_path:path} the `path` indicates that the parameter must
be a path.

You could need the parameter to contain /home/john_doe/myfile.txt, with a leading slash (/).

In that case, the URL would be: /files//home/john_doe/myfile.txt, with a double slash (//) 
between files and home.
"""


# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {"file_path": file_path}


"""
Query Parameters Section:

Query parameters are function parameters that are not passed in through the route.  They are
the parameters that come in from the url after the `?` and are separated by `&`.

They are naturally  strings because of the url but will be converted to the type declared in 
the function declaration.  Just like Path Parameters they come with:
    1. Data Parsing
    2. Data Validation (from pydantic)
    3. Automatic documentation ('url.../docs' | 'url.../redoc')
    
Adding defaults e.g. function(var_1: int = 0, var_2: int | None = None) will make the unaltered
route pass in the defaults.
"""

# fake_items_db: list[dict] = [
#     {"item_name": "Foo"},
#     {"item_name": "Bar"},
#     {"item_name": "Baz"},
# ]


# @app.get("/items_1/")
# async def read_item(skip: int = 0, limit: int = 10) -> list[dict]:
#     return fake_items_db[skip : skip + limit]


# Optional parameters
# @app.get("/items_2/{item_id}")
# async def read_item_2(item_id: str, q: str | None = None):
#     # Checks if q was passed in as a string and returns key, value pairs item_id and q
#     if q:
#         return {"item_id": item_id, "q": q}

#     # Base case returns just the item_id key, value pair
#     return {"item_id": item_id}


# Booleans can be converted as well
# @app.get("/items_3/{item_id}")
# async def read_item_3(item_id: str, q: str | None = None, short: bool = False):
#     """
#     Can use:
#         http://127.0.0.1:8000/items/foo?short=1
#         or
#         http://127.0.0.1:8000/items/foo?short=True
#         or
#         http://127.0.0.1:8000/items/foo?short=true
#         or
#         http://127.0.0.1:8000/items/foo?short=true
#         or
#         http://127.0.0.1:8000/items/foo?short=yes

#         or any other case variation (uppercase, first letter in uppercase, etc), your function will
#         see the parameter `short` with a `bool` value of `True`. Otherwise as `False`.
#     """
#     item: dict = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


# Multiple Query and Path Parameters
# app.get("/users/{user_id}/items/{item_id}")
# async def read_user_item(
#     user_id: int, item_id: str, q: str | None = None, short: bool = False
# ):
#     """
#     Multiple path and query parameters can be called at once.

#     They do not need to be declared in order, the name will be used to detect them.
#     """
#     item: dict = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


# Required Query Parameters
"""
Error (http://127.0.0.1:8000/items_4/foo-item):
{
    "detail": [
        {
            "type": "missing",
            "loc": [
                "query",
                "needy"
            ],
            "msg": "Field required",
            "input": null,
            "url": "https://errors.pydantic.dev/2.1/v/missing"
        }
    ]
}

Output (http://127.0.0.1:8000/items/foo-item?needy=sooooneedy):
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}


"""


# @app.get("/items_4/{item_id}")
# async def read_user_item_1(item_id: str, needy: str):
#     """To make a query parameter required, just don't set a default"""
#     item: dict = {"item_id": item_id, "needy": needy}
#     return item


# You can also pass in a combination of all of the above (required, optional, and default)


"""
Request Body Section

Data sent from a client to an API is called a Request Body. A Response Body is what is sent back to the client from
the API. Client's don't always need to send a Request Body. With FastAPI you use Pydantic models to declare Request 
Bodies. 
 
Usually you will use `POST` methods to send a Request Body, but `PUT`, `Delete`, and `PATCH` work.  
    - Sending a body with a `GET` request has an undefined behavior in the specifications, nevertheless, 
        it is supported by FastAPI, only for very complex/extreme use cases.
        
        
Use `Try It Now` in the docs to test!
"""

# First you need the BaseModel from Pydantic
from pydantic import BaseModel


# class Item(BaseModel):
#     """Creates data model (use None to make it optional)"""

#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.post("/items/")
# async def create_item(
#     item: Item,
# ):  # Declare the model as a parameter with type: model
#     return item


# Inside the function you can access all the item attributes directly
# @app.post("/items/")
# async def create_item(item: Item):
#     # Generate a dictionary representation of the model.  method dict() is deprecated
#     item_dict: dict = item.model_dump()

#     if item.tax:
#         price_with_tax: float = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})

#     return item_dict


"""
Query Parameters and String Validation Section

In Python 3.9+ Annotated is included, import from typing
    - `Annotated` can be used to add metadata to your parameters in
        This will:
            - Validate the data making sure that the max length is 50 characters
            - Show a clear error for the client when the data is not valid
            - Document the parameter in the OpenAPI schema path operation 
                (so it will show up in the automatic docs UI)
"""


# With Path Parameters
# @app.put("/items/{item_id}")
# async def create_item_with_path_parameters(item_id: int, item: Item):
#     return {"item_id": item_id, **item.model_dump()}


# Additional Validation
from typing import Annotated
from fastapi import Query


# app.get("/items/")
# async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
#     results: dict = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# Add Regular Expressions
# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         str | None,
#         Query(
#             min_length=3, max_length=50, pattern="^fixedquery$"
#         ),  # Must be exactly 'fixedquery'
#     ] = None
# ):
#     """
#     Before Pydantic version 2 and before FastAPI 0.100.0, the parameter was
#     called regex instead of pattern, but it's now deprecated.
#     """
#     results: dict = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# Using metadata and validation while making the parameter required, just don't set a default
# @app.get("/items/")
# async def read_items(q: Annotated[str, Query(min_length=3)]):
#     results: dict = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# You can be more explicit and set the default to a literal ellipsis
# @app.get("/items/")
# async def read_items(q: Annotated[str, Query(min_length=3)] = ...):  # Note the `...`
#     results: dict = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# Query Parameter List / Multiple Query Parameters
# @app.get("/items/")
# async def read_items(q: Annotated[list[str] | None, Query()] = None):
#     """Add Query in Annotated while declaring list as a type and it can handle multiple args"""
#     query_items = {"q": q}
#     return query_items


# http://localhost:8000/items/?q=foo&q=bar
# Output
# {
#   "q": [
#     "foo",
#     "bar"
#   ]
# }
# To declare a query parameter with a type of list, like in the example above, you need to
# explicitly use Query, otherwise it would be interpreted as a request body.

# With defaults: `q: Annotated[list[str], Query()] = ["foo", "bar"]`


# If you need a literally query that is not allowed in python, e.g. `item-query` (python `item_query`) use alias
# @app.get("/items/")
# async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
#     results: dict = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
