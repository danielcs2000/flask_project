from schemas.base_model import BaseModel
from uuid import UUID
from datetime import date
from typing import List
from schemas.utils import convert_date_to_iso_8601


class Institution(BaseModel):

    id: UUID
    name: str
    description: str
    address: str
    creation_date: date

    class Config:
        orm_mode = True
        json_encoders = {
            date: convert_date_to_iso_8601,
        }


class InstitutionCreateData(BaseModel):
    name: str
    description: str
    address: str
    creation_date: date


class InstitutionUpdateData(BaseModel):
    name: str
    description: str
    address: str


class Institutions(BaseModel):
    institutions: List[Institution]
