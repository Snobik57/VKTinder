from db.db_func import DbVkTinder


if __name__ == '__main__':
    #0. создаем объект класса, при инициализации запускается сессия с бд
    # !!! В конце необходимо обязательно вызвать db_vk_tinder.close() (см. п. 6)
    db_vk_tinder = DbVkTinder()

    #1. Добавление нового пользователя, не проверяется, есть ли уже, просто добавляет
    # db_vk_tinder.add_new_user(123, 'Vasiliy', 23, 'male', 'ekb')

    #2. Проверка по id_vk, есть ли такой пользователь в базе
    if db_vk_tinder.user_in_db(444):
        print('Он там есть!')
    else:
        print('Нет его')

    #3. add_variants_for_user - добавляет список вариантов для пользователя,
    # список вариантов - список словарей (в примере),
    # передается id_vk и список вариантов. Автоматически, если нужно добавляет в таблицу variants (если там еще нет),
    # и в таблицу UsersVariants (если уже есть)
    list_variants = [{'id_vk': 4454,
                      'name': 'Tatyana',
                      'age': 20,
                      'sex': 'female',
                      'city': 'Moscow'},
                     {'id_vk': 7777,
                      'name': 'Elena',
                      'age': 21,
                      'sex': 'female',
                      'city': 'Spb'}
                     ]

    db_vk_tinder.add_variants_for_user(123, list_variants)

    # 4. возвращает список id_vk - вариантов (которые уже были) для переданного id_vk
    list = db_vk_tinder.get_all_variants_for_user(123)
    print(list)

    # 5. возвращает True - если для переданного id_vk в вариантах есть второй параметр,
    # False - если нет (т.е. если данный id пользователю уже не подходит (уже был в поисках))
    print(db_vk_tinder.variant_in_db_for_user(123, 7777))
    print(db_vk_tinder.variant_in_db_for_user(123, 321))

    # 6. !!!! Обязательно использовать в конце, закрывает сессию с бд
    db_vk_tinder.close()

