# from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()
import os 

"""
dataset
ID (INT) primary key 
date_created datetime
url varchar (80) unique
download_link varchar (80) unique
base_folder_path varchar(100)
path varchar(100) 
Author_name varchar(50)
title varchar(100)
sub_title varchar(100)
about_dataset text
license varchar(100)
tags varchar(200)

"""
class Record(Base):
    __tablename__ = 'dataset_records'
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime(), default=datetime.utcnow, nullable=False, index=True)
    #url should be unique and not null 
    url = Column(String(255), nullable=False, unique=True)
    download_link = Column(String(255), nullable=False)
    base_folder_path = Column(String(255), nullable=False, index=True)
    path = Column(String(255), nullable=False, index=True)
    author_name = Column(String(255), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True, unique=True) 
    sub_title = Column(String(255), nullable=False, index=True)
    about_dataset = Column(Text, nullable=False, index=True)
    license = Column(String(255), nullable=False, index=True)
    tags = Column(String(255), nullable=False, index=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE_NAME = "datasets_db.db"
engine = create_engine("sqlite:///"+ os.path.join(BASE_DIR, DATABASE_FILE_NAME), echo=True)

session = sessionmaker()



