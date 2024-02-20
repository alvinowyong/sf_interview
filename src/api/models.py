from typing import List
from pydantic import BaseModel

class Address(BaseModel):
    ip: str

class Query(BaseModel):
    addresses: List[Address]
    client_ip: str
    created_at: int
    domain: str

class HealthResponse(BaseModel):
    message: str

class ReadRootResponse(BaseModel):
    version: str
    date: int
    kubernetes: bool

class ValidateIPRequest(BaseModel):
    ip: str

class ValidateIPResponse(BaseModel):
    status: bool

class HTTPError(BaseModel):
    message: str