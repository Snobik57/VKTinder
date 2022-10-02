import sqlalchemy as sq
import config as c
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from db_models import Users, Variants, UsersVariants, Photos, VariantsPhoto, create_tables


name_db = 'vk_tinder'

"""
Data Source Name.
Имя Источника Данных.
"""
DSN = f'postgresql://{c.USER}:{c.PASSWORD}@{c.HOST}:{c.PORT}/{name_db}'

"""
Connecting from database.
Подключение к базе данных.
"""
engine = sq.create_engine(DSN)

"""
If the database has not been created before, then creating it.
Если база данных не была создана ранее, то создаем ее.
"""
if not database_exists(engine.url):
    create_database(engine.url)

"""
For work with database creating session.
Создаем сессию для работы с базой данных.
"""
Ssesion = sessionmaker(bind=engine)
session = Ssesion()

"""
Creating models in database.
Создаем модели в базе данных.
"""
create_tables(engine)

"""
Closing session.
Закрываем сессию.
"""
session.close()
