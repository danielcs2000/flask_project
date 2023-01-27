from pydantic import BaseModel as _BaseModel
from typing import List, TypeVar, Type

from sqlalchemy.ext.declarative import DeclarativeMeta

T = TypeVar("T", bound="BaseModel")
M = TypeVar("M", bound=DeclarativeMeta)


class BaseModel(_BaseModel):
    @classmethod
    def from_single_orm(
        cls: Type[T],
        orm_object: DeclarativeMeta,
        **kwargs,
    ) -> T:
        """
        Convert an ORM object into its respective Pydantic schema
        """
        return super().from_orm(obj=orm_object)

    @classmethod
    def from_orms(
        cls: Type[T],
        orm_objects: List[M],
        **kwargs,
    ) -> List[T]:
        """
        Convert each of the ORM objects into their respective list of Pydantic schema.
        """
        return [cls.from_single_orm(orm_object=obj, **kwargs) for obj in orm_objects]
