import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True)
    id_vk = sq.Column(sq.Integer, nullable=False)
    name = sq.Column(sq.VARCHAR(100))
    age = sq.Column(sq.Integer, nullable=False)
    sex = sq.Column(sq.VARCHAR(30), nullable=False)
    city = sq.Column(sq.VARCHAR(100), nullable=False)


class Variants(Base):
    __tablename__ = 'variants'

    id = sq.Column(sq.Integer, primary_key=True)
    id_vk = sq.Column(sq.Integer, nullable=False)
    name = sq.Column(sq.VARCHAR(100))
    age = sq.Column(sq.Integer, nullable=False)
    sex = sq.Column(sq.VARCHAR(30), nullable=False)
    city = sq.Column(sq.VARCHAR(100), nullable=False)


class Photos(Base):
    __tablename__ = 'photos'

    id = sq.Column(sq.Integer, primary_key=True)
    link = sq.Column(sq.TEXT, nullable=False)
    size = sq.Column(sq.VARCHAR(10))


class UsersVariants(Base):
    __tablename__ = 'users_variants'

    id = sq.Column(sq.Integer, primary_key=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('users.id'), nullable=False)
    id_variant = sq.Column(sq.Integer, sq.ForeignKey('variants.id'), nullable=False)

    user = relationship('Users', backref='users_variants')
    variant = relationship('Variants', backref='users_variants')


class VariantsPhoto(Base):
    __tablename__ = 'variants_photos'

    id = sq.Column(sq.Integer, primary_key=True)
    variant_id = sq.Column(sq.Integer, sq.ForeignKey('variants.id'), nullable=False)
    photo_id = sq.Column(sq.Integer, sq.ForeignKey('photos.id'), nullable=False)

    variant = relationship('Variants', backref='variants_photos')
    photo = relationship('Photos', backref='variants_photos')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
