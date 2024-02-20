import time
import socket
import logging
import ipaddress
from typing import List

from fastapi import APIRouter
from fastapi import Request
from fastapi import HTTPException
from pymongo import MongoClient, DESCENDING

from api.models import ValidateIPRequest, ValidateIPResponse, HTTPError, Query, Address

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Client Definition for MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["interview"]
collection = db["query"]

v1_router = APIRouter()

@v1_router.get("/history", response_model=List[Query], responses={200: {"description": "OK", "model": List[Query]}, 400: {"model": HTTPError}})
async def queries_history():
    documents = collection.find().sort("created_at", DESCENDING).limit(20)
    query_models = [Query(**doc) for doc in documents]
    return query_models

@v1_router.get("/tools/lookup", response_model=Query, responses={200: {"description": "OK", "model": Query}, 400: {"model": HTTPError}, 404: {"model": HTTPError}})
async def lookup_domain(domain: str, request: Request):
    try:
        query_result = Query(
            # socket.gethostbyname_ex primarily returns only IPV4 addresses
            addresses=[Address(ip=ip) for ip in socket.gethostbyname_ex(domain)[2]],
            client_ip=request.client.host, 
            created_at=int(time.time()),
            domain=domain
        )

        result = collection.insert_one(query_result.model_dump())
        inserted_id = result.inserted_id
        logger.info(f"Query result inserted with ID: {inserted_id}")

        return query_result
    except socket.gaierror as e:
        # Catch gai (i.e. getaddrinfo()) error
        raise HTTPException(status_code=404, detail=f"Domain not found: {domain}")
    except Exception as e:
        # Catch all unforeseen edge-cases for exceptions using root-level Exception
        raise HTTPException(status_code=400, detail=f"Bad Request: {e}")

@v1_router.post("/tools/validate", response_model=ValidateIPResponse, responses={200: {"description": "OK", "model": ValidateIPResponse}, 400: {"model": HTTPError}})
async def validate_ip(req: ValidateIPRequest):
    # Utilise default ipaddress package to handle validation logic, easily extensible in the future
    try:
        ipaddress.IPv4Network(req.ip)
        return ValidateIPResponse(status=True)
    except ValueError:
        return ValidateIPResponse(status=False)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {e}")