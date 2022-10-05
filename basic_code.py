import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randrange
from datetime import datetime
from db.db_func import DbVkTinder

import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('token')
VKtoken = os.getenv('VKtoken')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
db_vk = DbVkTinder()


def write_msg(user_id, message, attachment=None, keyboard=None):
    params = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
    }
    if attachment is not None:
        params['attachment'] = attachment
    if keyboard is not None:
        params['keyboard'] = keyboard.get_keyboard()
    vk.method('messages.send', params)


# Получаем данные пользователя, который общается с ботом (год рождения, пол, город)
def get_user_info(user_id):
    ID = user_id
    URL = 'https://api.vk.com/method/users.get'
    params = {'user_ids': f'{ID}',
              'access_token': token,
              'v': '5.131',
              'fields': 'bdate, sex, city'
              }

    response = requests.get(url=URL, params=params).json()
    first_name = response.get('response')[0].get('first_name')
    last_name = response.get('response')[0].get('last_name')
    city = response.get('response')[0].get('city').get('id')
    gender = response.get('response')[0].get('sex')

    user_info = {'first_name': first_name,
                 'last_name':  last_name,
                 'city': city,
                 'gender': gender}
    return user_info


# Подбираем пары изходя из ранее полученных данных
def user_search(age_from=None, age_to=None):
    URL = 'https://api.vk.com/method/users.search'
    params = {'access_token': VKtoken,
              'v': '5.131',
              'sort': 0,
              'status': 6,
              'has_foto': 1,
              'city': get_user_info(event.user_id).get('city'),
              'sex': 1,
              'age_from': age_from,
              'age_to': age_to,
              'fields': 'bdate,sex'
              }
    response = requests.get(url=URL, params=params).json()
    return response.get('response')


# Получаем список фото пары в формате (количество лайков, id фото, url фото)
def get_user_photos(user_id):
    ID = user_id
    URL = 'https://api.vk.com/method/photos.get'
    params = {'owner_id': f'{ID}',
              'access_token': VKtoken,
              'v': '5.131',
              'album_id': 'profile',
              'rev': 0,
              'extended': 1,
              }
    response = requests.get(url=URL, params=params).json()
    likes_ids_list = []
    try:
        for photos in response.get('response').get('items'):
            for photo in photos.get('sizes'):
                if 'm' in photo.get('type'):
                    likes_ids = {'like': (photos.get('likes').get('count')),
                                 'photo_id': (photos.get('id')),
                                 'photo_url': (photo.get('url'))}
                    likes_ids_list.append(likes_ids)
        return likes_ids_list
    except AttributeError:
        return likes_ids_list


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        variant_info = []
        if event.to_me:
            request = event.text.lower()
            user_info = get_user_info(event.user_id)

            if request == "привет":
                write_msg(event.user_id,
                          f"{user_info['first_name']}, в каком году ты родился?")
            elif request.isdigit() and len(request) == 4:
                date = int(str(datetime.now())[:4]) - int(request)
                if not db_vk.user_in_db(event.user_id):
                    db_vk.add_new_user(event.user_id,
                                       name=f"{user_info['first_name']} {user_info['last_name']}",
                                       age=date,
                                       sex=user_info['gender'],
                                       city=user_info['city'])
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Найти Любовь", VkKeyboardColor.POSITIVE)
                write_msg(event.user_id,
                          f"{user_info['first_name']}, рада приветствовать вас!\n"
                          f" Для поиска пары нажмите кнокпу ниже)",
                          keyboard=keyboard)
            elif request == "найти любовь":

                age_user = db_vk.get_age_user(event.user_id)
                variants_list = user_search(age_from=age_user - 2,
                                            age_to=age_user + 2).get('items')
                for variant in variants_list:
                    variant_id = variant.get('id')
                    if not db_vk.variant_in_db_for_user(event.user_id, variant_id):
                        variant_info.append(variant)
                        photo = [x['photo_id'] for x in get_user_photos(variant_id)]
                        attachment_photo = [f'photo{variant_id}_{x}' for x in photo]
                        keyboard = VkKeyboard()
                        buttons = ['Дизлайк', 'Лайк', 'Далее']
                        button_collors = [VkKeyboardColor.NEGATIVE, VkKeyboardColor.POSITIVE, VkKeyboardColor.PRIMARY]

                        for button, button_collor in zip(buttons, button_collors):
                            keyboard.add_button(button, button_collor)
                        db_vk.add_new_variants(event.user_id,
                                               id_vk=variant_id,
                                               name=f"{variant.get('first_name')} {variant.get('last_name')}",
                                               age=variant.get('bdate'),
                                               sex=variant.get('sex'),
                                               city=user_info.get('city'),
                                               )
                        write_msg(event.user_id,
                                  f"{variant.get('first_name')} "
                                  f"{variant.get('last_name')}\n"
                                  
                                  f"Ссылка на профиль: https://vk.com/id"
                                  f"{variant_id}\n",
                                  attachment=','.join(attachment_photo),
                                  keyboard=keyboard)
                        break
                    else:
                        variant_info = []
                        continue

            elif request == 'лайк':
                variant_id = db_vk.count_new_variant(event.user_id)
                db_vk.new_status_for_variants(event.user_id, variant_id, 'LIKE')
            elif request == 'дизлайк':
                variant_id = db_vk.count_new_variant(event.user_id)
                db_vk.new_status_for_variants(event.user_id, variant_id, 'DISLIKE')
            elif request == 'далее':
                age_user = db_vk.get_age_user(event.user_id)
                variants_list = user_search(age_from=age_user - 2,
                                            age_to=age_user + 2).get('items')
                for variant in variants_list:
                    variant_id = variant.get('id')
                    if not db_vk.variant_in_db_for_user(event.user_id, variant_id):
                        variant_info.append(variant)
                        photo = [x['photo_id'] for x in get_user_photos(variant_id)]
                        attachment_photo = [f'photo{variant_id}_{x}' for x in photo]
                        db_vk.add_new_variants(event.user_id,
                                               id_vk=variant_id,
                                               name=f"{variant.get('first_name')} {variant.get('last_name')}",
                                               age=variant.get('bdate'),
                                               sex=variant.get('sex'),
                                               city=user_info.get('city'),
                                               )
                        write_msg(event.user_id, f"Вам может подойти {variant.get('first_name')} "
                                             f"{variant.get('last_name')}\n"
                                             f"Ссылка на профиль: https://vk.com/id"
                                             f"{variant.get('id')}\n",
                                             attachment=','.join(attachment_photo))
                        break
                    else:
                        variant_info = []
                    continue

            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не понял вашего ответа...")


