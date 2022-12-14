import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum

Base = declarative_base()


class Users(Base):
    """Дочерний класс от declarative_base. Хранит сведения о пользователе VK"""
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True)
    id_vk = sq.Column(sq.Integer, nullable=False)
    name = sq.Column(sq.VARCHAR(100))
    age = sq.Column(sq.Integer, nullable=False)
    sex = sq.Column(sq.VARCHAR(30), nullable=False)
    city = sq.Column(sq.VARCHAR(100), nullable=False)


class StatusType(Enum):
    """
    Creating a new data type to add variants in blacklist or whitelist.
    Создаем новый тип данных для добавления варантов в черный или белый список.
    """
    INERT = 1
    LIKE = 2
    DISLIKE = 3


class Variants(Base):
    """Дочерний класс от declarative_base. Хранит сведения о варианте найденом на платформе VK"""
    __tablename__ = 'variants'

    id = sq.Column(sq.Integer, primary_key=True)
    id_vk = sq.Column(sq.Integer, nullable=False)
    name = sq.Column(sq.VARCHAR(100))
    age = sq.Column(sq.VARCHAR(20), nullable=False)
    sex = sq.Column(sq.VARCHAR(30), nullable=False)
    city = sq.Column(sq.VARCHAR(100), nullable=False)


class UsersVariants(Base):
    """
    Дочерний класс от declarative_base. Хранит сведения о Users и Variants
    Необходим для создание связи "многие-ко-многим"
    """
    __tablename__ = 'users_variants'

    id = sq.Column(sq.Integer, primary_key=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('users.id'), nullable=False)
    id_variant = sq.Column(sq.Integer, sq.ForeignKey('variants.id'), nullable=False)
    status = sq.Column(sq.Enum(StatusType), nullable=False, default=StatusType.INERT.value)

    user = relationship('Users', backref='users_variants')
    variant = relationship('Variants', backref='users_variants')


def create_tables(engine):
    """Функция для создания моделей в БД"""
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    pass

