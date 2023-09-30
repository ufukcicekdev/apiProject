from fastapi import FastAPI, HTTPException, Request, Header, Request,Query
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader
from pydantic import BaseModel
from errors import InvalidAPIKeyError, DatabaseError, UnexpectedError
from utility.db import DBHelper
import psycopg2
from dotenv import load_dotenv
import adin_queries
from logger import log_to_db
import os
# Load the .env file
load_dotenv()



tags_metadata = [
    {
        "name": "adin.ai",
        "description": "Operations with users. The **login** logic is also here.",
    }
]


ADIN_API_KEY=os.getenv('ADIN_API_KEY')

app = FastAPI(openapi_tags=tags_metadata)

db_helper = DBHelper()


def verify_api_key(api_key: str):
    valid_api_key = ADIN_API_KEY # Geçerli API anahtarını burada tanımlayın

    if api_key != valid_api_key:
        raise InvalidAPIKeyError(status_code=401, detail="Invalid API key. Please provide a valid API key.")


class APIKeyHeader(BaseModel):
    api_key: str



@app.get("/adin_ai/get_data", tags=["adin.ai"])
async def get_data(api_key: str = Header(...)):
    try:
        verify_api_key(api_key)
        query = adin_queries.SELECT_ALL_DOMAINS_DATA
        data = db_helper.fetch(query)
        return {"data": data}
    except InvalidAPIKeyError as api_key_error:
        raise HTTPException(status_code=401, detail="Invalid API key. Please provide a valid API key.")
    except psycopg2.Error as db_error:
        log_to_db('ERROR', str(db_error), "adin api get_data")
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        log_to_db('ERROR', str(e), "adin api get_data")
        raise HTTPException(status_code=500, detail="Unexpected error.")
    



@app.get("/adin_ai/get_data_by_startdate_enddate", tags=["adin.ai"])
async def get_data_by_date(
    api_key: str = Header(...),
    start_date: str = Query(
        ...,  # Buraya başlangıç değerini ekleyebilirsiniz
        description="Start date in yyyy-mm-dd format (e.g., 2023-01-01)",
        regex=r"\d{4}-\d{2}-\d{2}",  # Tarih formatına uygunluk kontrolü eklemek için bir regex kullanabilirsiniz
    ),
    end_date: str = Query(
        ...,  # Buraya başlangıç değerini ekleyebilirsiniz
        description="End date in yyyy-mm-dd format (e.g., 2023-12-31)",
        regex=r"\d{4}-\d{2}-\d{2}",  # Tarih formatına uygunluk kontrolü eklemek için bir regex kullanabilirsiniz
    ),
    domain_id: int = Query(..., description="Domain Id")

):
    try:
        verify_api_key(api_key)
        values = (start_date, end_date, domain_id)
        data = db_helper.fetch(adin_queries.SELECT_DATA_BY_DATE, values)
        return {"data": data}
    except InvalidAPIKeyError as api_key_error:
        raise HTTPException(status_code=401, detail="Invalid API key. Please provide a valid API key.")
    except psycopg2.Error as db_error:
        log_to_db('ERROR', str(db_error), "adin api get_data_by_date")
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        log_to_db('ERROR', str(e), "adin api get_data_by_date")
        raise HTTPException(status_code=500, detail="Unexpected error.")





@app.get("/adin_ai/get_data_by_createdate", tags=["adin.ai"])
async def get_data_by_date(
    api_key: str = Header(...),
    create_date: str = Query(
        ...,  # Başlangıç değerini buraya ekleyebilirsiniz
        description="Start date in yyyy-mm-dd format (e.g., 2023-01-01)",
        regex=r"\d{4}-\d{2}-\d{2}",  # Tarih formatına uygunluk kontrolü için regex kullanabilirsiniz
    ),
):
    try:
        verify_api_key(api_key)
        query = adin_queries.SELECT_DATA_BY_CREATEDATE
        values = (create_date,)
        data = db_helper.fetch(query, values)
        return {"data": data}
    except InvalidAPIKeyError as api_key_error:
        raise HTTPException(status_code=401, detail="Invalid API key. Please provide a valid API key.")
    except psycopg2.Error as db_error:
        log_to_db('ERROR', str(db_error), "adin api get_data_by_createdate")
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        log_to_db('ERROR', str(e), "adin api get_data_by_createdate")
        raise HTTPException(status_code=500, detail="Unexpected error.")


@app.get("/adin_ai/get_data_by_createdate_domainid", tags=["adin.ai"])
async def get_data_by_date(
    api_key: str = Header(...),
    create_date: str = Query(
        ...,  # Buraya başlangıç değerini ekleyebilirsiniz
        description="Start date in yyyy-mm-dd format (e.g., 2023-01-01)",
        regex=r"\d{4}-\d{2}-\d{2}",  # Tarih formatına uygunluk kontrolü eklemek için bir regex kullanabilirsiniz
    ),
    domain_id: int = Query(..., description="Domain Id")

):
    try:
        verify_api_key(api_key)
        values = (create_date, domain_id)
        data = db_helper.fetch(adin_queries.SELECT_DATA_BY_CREATEDATE_DOMAINID, values)
        return {"data": data}
    except InvalidAPIKeyError as api_key_error:
        raise HTTPException(status_code=401, detail="Invalid API key. Please provide a valid API key.")
    except psycopg2.Error as db_error:
        log_to_db('ERROR', str(db_error), "adin api get_data_by_date")
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        log_to_db('ERROR', str(e), "adin api get_data_by_date")
        raise HTTPException(status_code=500, detail="Unexpected error.")