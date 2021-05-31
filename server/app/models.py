from datetime import datetime
from pydantic import BaseModel


class UserIn(BaseModel):
    platform: str
    user_name: str
    token: str


class User(BaseModel):
    id: int
    platform: str
    user_name: str
    token: str
    created_at: datetime


class JobIn(BaseModel):
    command: str
    exit_code: int
    os: str
    prompt: str
    seconds: float
    user_id: int


class Job(BaseModel):
    id: int
    command: str
    exit_code: int
    os: str
    prompt: str
    seconds: float
    user_id: int
    created_at: datetime
