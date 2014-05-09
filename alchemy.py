from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'phonebook'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    number = Column(String(20), nullable=False)

engine = create_engine('sqlite:///sqlalchemy_phonebook.db')
Base.metadata.create_all(engine)