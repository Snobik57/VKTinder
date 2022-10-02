import sqlalchemy as sq
import db.config as c
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from db.db_models import Users, Variants, UsersVariants, Photos, VariantsPhoto, create_tables

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

    def add_variants_for_user(self, id_vk, list_variants):

        user_id = self.get_id_user(id_vk)
        if user_id is None:
            return False

        list_id_vk = []
        for variant in list_variants:
            list_id_vk.append(variant['id_vk'])

        list_id = []
        q = self.session.query(Variants).filter(Variants.id_vk.in_(list_id_vk))
        for variant in q.all():
            list_id.append({'id_vk': variant.id_vk,
                            'id': variant.id})
            list_id_vk.remove(variant.id_vk)

        # Добавление новых объектов в variants
        for variant in list_variants:
            if variant['id_vk'] in list_id_vk:
                new_variant = Variants(id_vk=variant['id_vk'], name=variant['name'], age=variant['age'],
                                       sex=variant['sex'], city=variant['city'], status='INERT')

                self.session.add(new_variant)
                self.session.commit()

                list_id.append({'id_vk': new_variant.id_vk,
                                'id': new_variant.id})

        # Добавление связей
        for dict_id in list_id:
            q = self.session.query(UsersVariants).filter(UsersVariants.id_user == user_id).filter(
                                                         UsersVariants.id_variant == dict_id['id'])
            empty_record = True
            for res in q.all():
                empty_record = False

            if empty_record:
                new_Users_Variants = UsersVariants(id_user=user_id, id_variant=dict_id['id'])
                self.session.add(new_Users_Variants)
                self.session.commit()


        return True

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
