#!flask/bin/python
# -*- coding: UTF-8 -*-

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

DB_URI = 'sqlite:///./Patients.db'
Base = declarative_base()

class Pessoas(Base):
    __tablename__ = 'pessoas'

    id   = Column(Integer, primary_key=True)
    nome = Column(String(80))

if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

