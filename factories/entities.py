from factory.alchemy import SQLAlchemyModelFactory
from model.entities import User, Institution, Project
import factory
from faker import Faker
from faker.providers import BaseProvider
from datetime import date, timedelta, datetime


import factory.fuzzy as fuzzy

from database import connector

db = connector.Manager()
engine = db.createEngine()

db_session = db.getSession(engine)


class Provider(BaseProvider):
    def random_birthday(self, age: int) -> date:
        return fuzzy.FuzzyDate(
            start_date=datetime.now() - timedelta(days=(age + 1) * 365),
            end_date=datetime.now() - timedelta(days=age * 365),
        ).fuzz()

    def random_end_date(self) -> date:
        return fuzzy.FuzzyDate(
            start_date=datetime.now() + timedelta(days=2),
            end_date=datetime.now() + timedelta(days=100),
        ).fuzz()


faker = Faker()
faker.add_provider(Provider)


class InstitutionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Institution
        sqlalchemy_session = db_session
        sqlalchemy_session_persistence = "commit"

    name = factory.Sequence(lambda n: "Institution %d" % n)
    description = factory.Sequence(lambda n: "Description %d" % n)
    address = factory.LazyAttribute(lambda _: faker.address())
    creation_date = faker.date_of_birth()


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db_session
        sqlalchemy_session_persistence = "commit"

    name = factory.LazyAttribute(lambda _: faker.name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    RUT = factory.LazyAttribute(
        lambda _: faker.unique.pystr_format(string_format="#" * 8)
    )
    age = factory.LazyAttribute(lambda _: faker.pyint(min_value=15, max_value=40))
    birthday = factory.LazyAttribute(lambda user: faker.random_birthday(age=user.age))
    job_tittle = factory.LazyAttribute(lambda _: faker.last_name())


class ProjectFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Project
        sqlalchemy_session = db_session
        sqlalchemy_session_persistence = "commit"

    name = factory.Sequence(lambda n: "Project %d" % n)
    description = factory.Sequence(lambda n: "Description %d" % n)
    creation_date = factory.LazyAttribute(lambda _: faker.random_birthday(age=2))
    end_date = factory.LazyAttribute(lambda _: faker.random_end_date())
