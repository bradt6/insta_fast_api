from fastapi import Depends, FastAPI, HTTPException, Query, status 
from typing import List, Match, Optional, Tuple
from databases import Database
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import user
from database import get_database, sqlalchemy_engine
from models import User, metadata, users


app = FastAPI()

@app.on_event("startup")
async def startup():
    await get_database().connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()


async def get_user_or_404(
    id: int, database: Database = Depends(get_database)
) -> User:
    select_query = users.select().where(users.c.id == id)
    user = await database.fetch_one(select_query)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return User(**user)

# pagination values defauls set at 0 and query default set to 10 
async def pagination(skip: int = Query(0, ge=0),limit: int = Query(10, ge=0),) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)

@app.get("/users")
async def list_users(pagination: Tuple[int, int] = Depends(pagination),
    database: Database = Depends(get_database),
    next_page_token: Optional[int] = None,
    before_page_token: Optional[int] = None):
    select_query = None
    before_val = 0
    if next_page_token:
        skip, limit = pagination
        select_query = users.select().offset(next_page_token).limit(limit)
        #This is a bad way of implementing this. This should be done based on last ID,  cache or timestamp(modified date)
        # assumes the limit is remianing constant
        before_val = next_page_token - limit 
        next_page_token = next_page_token + limit
    elif before_page_token:
        skip, limit = pagination
        select_query = users.select().offset(before_page_token).limit(limit)
        before_val = before_page_token - limit 
        next_page_token = before_page_token + limit 
    else:
        skip, limit = pagination
        select_query = users.select().offset(skip).limit(limit)

    rows = await database.fetch_all(select_query)

    if before_val < 0:
        before_val = 0
    if not next_page_token:
        next_page_token = skip + limit

    results = [User(**row) for row in rows]
    json_result = {
        "data": results,
        "meta": {
            "continuation-token-after": next_page_token,
            "continuation-token-before": before_val
        }
    }
    return json_result

@app.get("/users/{id}", response_model=User)
async def get_user(user: User = Depends(get_user_or_404)) -> User:
    return user

# Original list users without anypagination tokens build into the functionality 

# @app.get("/users")
# async def list_users(
#     pagination: Tuple[int, int] = Depends(pagination),
#     database: Database = Depends(get_database),
# ) -> List[User]:
#     skip, limit = pagination
#     select_query = users.select().offset(skip).limit(limit)
#     rows = await database.fetch_all(select_query)

#     results = [User(**row) for row in rows]
    
#     return results
