import sqlalchemy as sq
import config as c
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from db_models import Users, Variants, UsersVariants, Photos, VariantsPhoto, create_tables


name_db = 'vk_tinder'
DSN = f'postgresql://{c.USER}:{c.PASSWORD}@{c.HOST}:{c.PORT}/{name_db}'
engine = sq.create_engine(DSN)

if not database_exists(engine.url):
    create_database(engine.url)

Ssesion = sessionmaker(bind=engine)
session = Ssesion()

create_tables(engine)

session.close()