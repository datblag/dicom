from config import sqllite_base_path

from sqlalchemy import create_engine, MetaData, Column, INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = create_engine(r'''sqlite:///'''+sqllite_base_path+'''''', echo=True)
Base = declarative_base()
metadata = MetaData()
session = Session(bind=engine)


class Files(Base):
    __tablename__ = 'files'
    file_id = Column(INTEGER, primary_key=True)
    file_name = Column(VARCHAR(250))
    file_catalog = Column(VARCHAR(50))


#Base.metadata.create_all(engine)
