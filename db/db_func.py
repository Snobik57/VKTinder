import sqlalchemy as sq
import curse_project_VKTinder.db.config as c
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy_utils import database_exists, create_database
from curse_project_VKTinder.db.db_models import Users, Variants, UsersVariants, create_tables

name_db = 'vk_tinder'
DSN = f'postgresql://{c.USER}:{c.PASSWORD}@{c.HOST}:{c.PORT}/{name_db}'


class DbVkTinder:
    def __init__(self):
        engine = sq.create_engine(DSN)

        if not database_exists(engine.url):
            create_database(engine.url)
            create_tables(engine)

        Ssesion = sessionmaker(bind=engine)
        self.session = Ssesion()

    def add_new_user(self, id_vk, name, age, sex, city):
        new_user = Users(id_vk=id_vk, name=name, age=age, sex=sex, city=city)
        self.session.add(new_user)
        self.session.commit()

        return True

    def user_in_db(self, id_vk):
        q = self.session.query(Users).filter(Users.id_vk == id_vk)
        result = False
        for res in q.all():
            result = True
            break
        return result

    def get_id_user(self, id_vk):
        q = self.session.query(Users).filter(Users.id_vk == id_vk)
        result = None
        for res in q.all():
            result = res.id
            break

        return result

    def get_age_user(self, id_vk):
        q = self.session.query(Users).filter(Users.id_vk == id_vk)
        result = None
        for res in q.all():
            result = res.age
            break

        return result

    def add_new_variants(self, user_id_vk, status="INERT", **kwargs,):
        user_id = self.get_id_user(user_id_vk)
        new_variants = Variants(id_vk=kwargs['id_vk'],
                                name=kwargs['name'],
                                age=kwargs['age'],
                                sex=kwargs['sex'],
                                city=kwargs['city'],
                                )
        self.session.add(new_variants)
        q = self.session.query(Variants).filter(Variants.id_vk == kwargs['id_vk'])
        id = None
        for row in q:
            id = row.id
            break
        new_users_variants = UsersVariants(id_user=user_id, id_variant=id, status=status)
        self.session.add(new_users_variants)
        self.session.commit()

        return True

    def new_status_for_variants(self, user_id_vk, variants_id, status):
        query_id_user = self.session.query(Users.id).where(Users.id_vk == user_id_vk).one()

        query = self.session.query(UsersVariants)
        query = query.filter(UsersVariants.id_user == query_id_user[0]).\
            filter(UsersVariants.id_variant == variants_id).\
            update({'status': status})
        self.session.commit()

    def count_new_variant(self, user_id_vk):
        query_max = self.session.query(func.max(UsersVariants.id_variant)).join(Users)
        query_max = query_max.where(Users.id_vk == user_id_vk).one()

        return query_max[0]

    def get_all_variants_for_user(self, id_vk):
        list_id = []
        q = self.session.query(Users).join(UsersVariants.user)\
            .join(Variants, UsersVariants.id_variant == Variants.id).filter(Users.id_vk == id_vk)
        for res in q.all():
            for var in res.users_variants:
                list_id.append(var.variant.id_vk)

        return list_id

    def variant_in_db_for_user(self, id_vk, id_vk_variant):
        q = self.session.query(Users).join(UsersVariants.user) \
            .join(Variants, UsersVariants.id_variant == Variants.id).filter(Users.id_vk == id_vk)\
            .filter(Variants.id_vk == id_vk_variant)

        result = False
        for res in q.all():
            result = True

        return result

    def close(self):
        self.session.close()


if __name__ == "__main__":
    pass
