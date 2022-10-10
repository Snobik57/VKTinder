import os
import requests
import vk_api
import vk_api.keyboard
from random import randrange
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll
from db.db_func import DbVkTinder


load_dotenv()

token = os.getenv('token')
VKtoken = os.getenv('VKtoken')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
db_vk = DbVkTinder()


def write_msg(user_vk_id: str or int, message: str, attachment=None, keyboard=None) -> dict:
    """
    Функция отправляет сообщение через VK API указанному пользователю VK

    params: user_id: str or int - ID пользователя VK
    params: message: str - Сообщение, которое необходимо отправить.
    params: attachment: str - Необязательный параметр, отправляет фотографии указанные пользователем
    params: keyboard: str - Необязательный параметр, задействует метод VK API и отправляет кнопки указанные пользователем

    :return: dict: если запрос успешный - {'result': True, 'id_msg': response}
                   если запрос провальный - {'result': False, 'error': response}
    """
    params = {
        'user_id': user_vk_id,
        'message': message,
        'random_id': randrange(10 ** 7),
    }

    if attachment is not None and isinstance(attachment, str):
        params['attachment'] = attachment
    if keyboard is not None and isinstance(keyboard, vk_api.keyboard.VkKeyboard):
        params['keyboard'] = keyboard.get_keyboard()

    response = vk.method('messages.send', params)

    return {'result': isinstance(response, int), 'id_msg': response}


def get_user_info(user_vk_id: str or int) -> dict:
    """
    Функция позволяет получить данные пользователя VK, используя метод VK API users.get. (имя, фамилия, пол, город).
    :params user_vk_id: str or int - ID пользователя VK

    :return: dict - {'vk_id': int, 'first_name': srt, 'last_name': str, 'sex': int
                    'city_id': int, 'city':  str ,'birth_date': str}
    """
    url = 'https://api.vk.com/method/users.get'
    params = {'user_ids': f'{user_vk_id}',
              'access_token': token,
              'v': '5.131',
              'fields': 'bdate, sex, city'
              }

    response = requests.get(url=url, params=params).json()
    first_name = response.get('response')[0].get('first_name')
    last_name = response.get('response')[0].get('last_name')
    city = response.get('response')[0].get('city')
    if city is not None:
        city = city.get('id')
    gender = response.get('response')[0].get('sex')

    user_info = {'first_name': first_name,
                 'last_name': last_name,
                 'city': city,
                 'gender': gender}
    return user_info


def user_search(user_vk_id: str or int, age_from=None, age_to=None) -> list:
    """
    Функция позволяет получить список словарей с данными пользователей по указанным параметрам, использу метод
    VK API users.search. (имя, фамилия, город, пол, дата рождения)
    :params user_vk_id: str or int - ID пользователя VK
    :params age_from: str or int - Необязательный параметр, с какого возраста начать поиск
    :params age_to: str or int - Необязательный параметр, по какой возраст начать поиск

    :return: [
                'count': count,
                'items': {'vk_id': int, 'first_name': srt, 'last_name': str, 'sex': int
                             'city_id': int, 'city':  str ,'birth_date': str, 'age': int , photos": str}
            ]
    """
    info_user = get_user_info(user_vk_id)
    if info_user.get('sex') == 1:
        sex = 2
    else:
        sex = 1
    URL = 'https://api.vk.com/method/users.search'
    params = {'access_token': VKtoken,
              'v': '5.131',
              'sort': 0,
              'status': 6,
              'has_foto': 1,
              'city': info_user.get('city'),
              'sex': sex,
              'age_from': age_from,
              'age_to': age_to,
              'fields': 'bdate,sex',
              'count': 1000
              }
    response = requests.get(url=URL, params=params).json()
    return response.get('response')


def get_user_photos(user_vk_id: str or int) -> list:
    """
    Функция позволяет получить фотографии указанного профиля VK, с помощью метода VK API photos.get
    (количество лайков, ID фото, URL фото)
    :params user_vk_id: str or int - ID пользователя VK

    :return: list - [{'like': like, 'photo_id': photo_id, 'photo_url': photo_url}]
    """
    url = 'https://api.vk.com/method/photos.get'
    params = {'owner_id': f'{user_vk_id}',
              'access_token': VKtoken,
              'v': '5.131',
              'album_id': 'profile',
              'rev': 0,
              'extended': 1,
              }
    response = requests.get(url=url, params=params).json()
    likes_ids_list = []
    if response.get('response').get('items') is not None:
        for photos in response.get('response').get('items'):
            for photo in photos.get('sizes'):
                if 'm' in photo.get('type'):
                    likes_ids = {'like': (photos.get('likes').get('count')),
                                 'photo_id': (photos.get('id')),
                                 'photo_url': (photo.get('url'))}
                    if len(likes_ids_list) < 3:
                        likes_ids_list.append(likes_ids)
                    else:
                        break
        return sorted(likes_ids_list, key=lambda x: x.get('like'), reverse=True)
    else:
        return likes_ids_list


if __name__ == "__main__":
    pass


