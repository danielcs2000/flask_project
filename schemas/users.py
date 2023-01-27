from schemas.base_model import BaseModel

from datetime import date
from uuid import UUID

from typing import List

from schemas.utils import convert_date_to_iso_8601
from schemas.projects import Project


class User(BaseModel):
    id: UUID
    name: str
    last_name: str
    RUT: str
    birthday: date
    job_tittle: str
    age: int

    class Config:
        orm_mode = True
        json_encoders = {
            date: convert_date_to_iso_8601,
        }


class UserWithProjects(BaseModel):
    id: UUID
    name: str
    last_name: str
    RUT: str
    birthday: date
    job_tittle: str
    age: int
    projects: List[Project]

    class Config:
        orm_mode = True
        json_encoders = {
            date: convert_date_to_iso_8601,
        }


class Users(BaseModel):
    users: List[User]
