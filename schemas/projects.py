from uuid import UUID
from datetime import date
from schemas.base_model import BaseModel
from typing import List
from schemas.utils import convert_date_to_iso_8601


class Project(BaseModel):
    id: UUID
    name: str
    description: str
    creation_date: date
    end_date: date
    user_id: UUID
    institution_id: UUID

    class Config:
        orm_mode = True
        json_encoders = {
            date: convert_date_to_iso_8601,
        }


class Projects(BaseModel):
    projects: List[Project]


class ProjectWithDaysLeft(Project):
    days_left: int
