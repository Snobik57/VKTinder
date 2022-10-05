import vk_api
import os
import requests
from dotenv import load_dotenv
from random import randrange

load_dotenv()

token = os.getenv('token')
VKtoken = os.getenv('VKtoken')

vk = vk_api.VkApi(token=token)


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
                 'last_name': last_name,
                 'city': city,
                 'gender': gender}
    return user_info


# Подбираем пары изходя из ранее полученных данных
def user_search(user_vk_id, age_from=None, age_to=None):
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


if __name__ == "__main__":
    pass
