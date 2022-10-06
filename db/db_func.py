import sqlalchemy as sq
import db.config as c
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy_utils import database_exists, create_database
from db.db_models import Users, Variants, UsersVariants, create_tables

name_db = 'vk_tinder'
DSN = f'postgresql://{c.USER}:{c.PASSWORD}@{c.HOST}:{c.PORT}/{name_db}'


class DbVkTinder:
    """
    Класс для взаимодействия с базой данных vk_tinder с помощью библиотеки SQLalchemy
    """
    def __init__(self):
        """При создании экземпляра класса, создается БД, таблицы в ней и открывается сессия для работы с ней.
        engine:  Функция sqlalchemy.create_engine() создает новый экземпляр класса sqlalchemy.engine.
                 Engine который предоставляет подключение к базе данных.
        create_database: Создание БД
        create_tables: Создание таблиц в БД
        session: экземпляр класса sqlalchemy.orm sessionmaker создает подключение к текущей БД
        """
        engine = sq.create_engine(DSN)

        if not database_exists(engine.url):
            create_database(engine.url)
            create_tables(engine)

        Ssesion = sessionmaker(bind=engine)
        self.session = Ssesion()

    def add_new_user(self, id_vk: str, name: str, age: str or int, sex: int, city: int) -> bool:
        """
        Метод класса позволяет добавить данные о новом пользователе в таблицу Users
        :params id_vk: str - ID пользователя VK
        :params name: str - Имя и Фамилия пользователя VK
        :params age: str - возраст пользователя VK
        :params sex: str - идентификатор пола пользователя VK
        :params city: str - идентификатор города пользователя VK

        :return: bool True
        """
        new_user = Users(id_vk=id_vk, name=name, age=age, sex=sex, city=city)
        self.session.add(new_user)
        self.session.commit()

        return True

    def user_in_db(self, id_vk: str) -> bool:
        """
        Метод класса позволяет проверить существует ли данные об этом пользователе VK, по его ID
        :params id_vk: str - ID пользователя VK

        :return: bool - True если данный id_vk найдет в таблице Users
                        False если данный id_vk не найден в таблице Users
        """
        q = self.session.query(Users).filter(Users.id_vk == id_vk)
        result = False
        for res in q.all():
            result = True
            break
        return result

    def get_id_user(self, id_vk: str) -> int:
        """
        Метод класса позволяет получить Users.id по ID VK пользователя
        :params id_vk: str - ID пользователя VK

        :return: int - Если данный ID пользователя обнаружен в БД
                 None - Если данный ID пользователя не обнаружен в БД
        """
        q = self.session.query(Users).filter(Users.id_vk == id_vk)
        result = None
        for res in q.all():
            result = res.id
            break

        return result

    def get_age_user(self, id_vk: str) -> str:
        """
        Метод класса позволяет получить Users.age по ID VK пользователя
        :params id_vk: str - ID пользователя VK

        :return: str - Если данный ID пользователя обнаружен в БД
                 None - Если данный ID пользователя не обнаружен в БД
        """
        q = self.session.query(Users).filter(Users.id_vk == id_vk)
        result = None
        for res in q.all():
            result = res.age
            break

        return result

    def add_new_variants(self, user_id_vk: str, status="INERT", **kwargs) -> bool:
        """
        Метод класса позволяет добавить данные о новом варианте в таблицу Variants
        и создать связь в таблиые UsersVariants
        :params user_id_vk: str - ID пользователя VK
        :params status: str - Необязятельный параметр, для добавления статуса варианта в UsersVariants
        :kwargs: dict - Ожидает словарь со следующими ключами и значениями:

        {'id_vk': kwargs['id_vk'],
         'name': kwargs['name'],
         'age': kwargs['age'],
         'sex': kwargs['sex'],
         'city': kwargs['city']}

        :params id_vk: str - ID пользователя VK
        :params name: str - имя и фамилия пользователя VK
        :params age: str - возраст пользователя VK
        :params sex: int - идентификатор пола пользователя VK
        :params city: int - идентификатор города пользователя VK

        :return: bool True
        """
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

    def new_status_for_variants(self, user_id_vk: str, variants_id: str, status: str) -> None:
        """
        Метод класса позволяющий обновить статус варианта в таблице UsersVariants

        :params user_id_vk: str - ID пользователя VK
        :params variants_id: str - ID пользователя VK
        :params status: str - тип данных для БД наследованный от класса Enum: INERT = 1
                                                                              LIKE = 2
                                                                              DISLIKE = 3

        query_id_user - SELECT Запрос на получение Users.id
        query - UPDATE Запрос для обновления UsersVariants.status
        """
        query_id_user = self.session.query(Users.id).where(Users.id_vk == user_id_vk).one()

        query = self.session.query(UsersVariants)
        query = query.filter(UsersVariants.id_user == query_id_user[0]).\
            filter(UsersVariants.id_variant == variants_id).\
            update({'status': status})
        self.session.commit()

    def count_new_variant(self, user_id_vk: str) -> int:
        """
        Метод класса для нахождения новоой записи в таблице UsersVariants

        :params user_id_vk: str - ID пользователя VK

        :return: int - UsersVariants.id_variant
        """
        query_max = self.session.query(func.max(UsersVariants.id_variant)).join(Users)
        query_max = query_max.where(Users.id_vk == user_id_vk).one()

        return query_max[0]

    def get_all_variants_for_user(self, id_vk: str) -> list:
        """
        Метод для нахождения всех добавленных вариантов в UsersVariants для опеределенного пользователя

        :params id_vk: str - ID пользователя VK

        q - SELECT запрос для получения всех записей для пользователя VK, по его ID.
        list_id - Список наполненный всеми записями Variants.id_vk для конкретного пользователя

        :return: list - list_id
        """
        list_id = []
        q = self.session.query(Users).join(UsersVariants.user)\
            .join(Variants, UsersVariants.id_variant == Variants.id).filter(Users.id_vk == id_vk)
        for res in q.all():
            for var in res.users_variants:
                list_id.append(var.variant.id_vk)

        return list_id

    def variant_in_db_for_user(self, id_vk: str, id_vk_variant: str) -> bool:
        """
        Метод для нахождения указанного варината для конкретного пользователя.

        :params id_vk: str - ID пользователя VK
        :params id_vk_variant: str - ID пользователя VK

        q - SELECT запрос для получения записи из таблиц Users и Variants о указанном
        варианте для указанного пользователя.

        :return: bool - True - если запись есть
                        False - если записи нет
        """
        q = self.session.query(Users).join(UsersVariants.user) \
            .join(Variants, UsersVariants.id_variant == Variants.id).filter(Users.id_vk == id_vk)\
            .filter(Variants.id_vk == id_vk_variant)

        result = False
        for res in q.all():
            result = True

        return result

    def close(self) -> None:
        """
        Метод для закрытия текущей сессии

        :return: None
        """
        self.session.close()


if __name__ == "__main__":
    pass
