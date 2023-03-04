from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

engine = create_engine(config('PSQL_secure_data'), echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class KijijiData(Base):
    __tablename__ = "parsed_data"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    currency = Column(String(2))
    price = Column(String(20))
    location = Column(String(50))
    date = Column(String(20))
    image = Column(String())


Base.metadata.create_all(engine)
