from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from datetime import date
from uuid import UUID


class Manager:
    Base = declarative_base()
    session = None

    def createEngine(self):
        engine = create_engine(
            "postgresql://postgres:postgres@postgres:5432/postgres",
        )
        self.Base.metadata.create_all(engine)
        return engine

    def getSession(self, engine):
        if self.session is None:
            Session = sessionmaker(bind=engine)
            session = Session()
        return session


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [
                x for x in dir(obj) if not x.startswith("_") and x != "metadata"
            ]:
                data = obj.__getattribute__(field)
                print(data)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:

                    if isinstance(data, UUID):
                        fields[field] = str(data)
                    elif isinstance(data, date):
                        fields[field] = data.strftime("%m/%d/%Y, %H:%M:%S")
                    else:
                        fields[field] = None

            return fields

        return json.JSONEncoder.default(self, obj)
