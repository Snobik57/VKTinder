import random
from pprint import pprint
from random import randrange

from get_token import get_token
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = 'vk1.a.ou1fBJqpxvKat-yWw0ylJQWbYMV5t2LrIPPI_zHvgCW2wGEFmCEVs1-MvxIUq_YW0_BXRiTtSwJyuZvkFpBqXe7miNZIkbwN4xrs1nhY7hAx4pvLPHxKM7yJNM2lwAVfY8EifGObHvYzuY-4dkzBAKagnCxqsuPv_HUyrEXfF3tYOZjBaRG_aMTOiIk8nsl_'
VKtoken = 'vk1.a.ZFlUIyFDWCMDuOQJTnkdvb8dBTrKBLXw2TCcQus72RMdsBztc-7LxMVMh8KXmOr5NI_JiROmckWcROMmPtQAH7ZYkRBpNPvqTu_YDPaIvWUue81J2QLFcV1jltMtgUDkOCOsdYKHiS-PmtVtyw3UrrBdDT0ci4c3_suWY56EJUl5wcO5G8aemVuFznhWGPBL'

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, attachment=None):
    params = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
    }
    if attachment is not None:
        params['attachment'] = attachment
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
    # bdate = response.get('response')
    # дата фиксированная
    bdate = '01.01.1995'
    city = response.get('response')[0].get('city').get('id')
    gender = response.get('response')[0].get('sex')
    user_info = {'age': bdate[-4:], 'city': city, 'gender': gender}
    return user_info

# Подбираем пары изходя из ранее полученных данных
def user_search():
    URL = 'https://api.vk.com/method/users.search'
    params = {'access_token': VKtoken,
              'v': '5.131',
              'sort': 0,
              'status': 6,
              'has_foto': 1,
              'city': get_user_info(event.user_id).get('city'),
              'sex': 1,
              'birth_year': get_user_info(event.user_id).get('age')
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


# Отправляем фото в чат. Пока только одно(((
# Теперь этот метод не особо нужен.
def send_photo(owner_id, photo_id):
    ID = event.user_id
    URL = 'https://api.vk.com/method/messages.send'
    params = {'user_id': f'{ID}',
              'random_id': 0,
              'access_token': VKtoken,
              'v': '5.131',
              'attachment': f'photo{owner_id}_{photo_id}'
              }
    response = requests.get(url=URL, params=params)
    return f'Чтобы показать следующий результат напишите "далее"'



for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == 'авторизироваться':
                write_msg(event.user_id, f"пройдите по этой ссылке:\n"
                                         f"https://oauth.vk.com/authorize?client_id=8208525&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos,offline&response_type=token&v=5.131&state=123456")
            elif request == "найти пару":
                get_user_info(event.user_id)
                variant = user_search().get('items')[0]
                variant_id = variant.get('id')
                photo = [x['photo_id'] for x in get_user_photos(variant_id)]
                attachment_photo = [f'photo{variant_id}_{x}' for x in photo]
                write_msg(event.user_id,
                          f"{variant.get('first_name')} "
                          f"{variant.get('last_name')}\n"
                          f"Ссылка на профиль: https://vk.com/id"
                          f"{variant_id}\n",
                          attachment=','.join(attachment_photo))

            elif request == 'далее':
                counter = random.randrange(1, len(user_search().get('items')))
                variant = user_search().get('items')
                variant_id = variant[counter].get('id')
                photo = [x['photo_id'] for x in get_user_photos(variant_id)]
                attachment_photo = [f'photo{variant_id}_{x}' for x in photo]
                write_msg(event.user_id, f"Вам может подойти {variant[counter].get('first_name')} "
                                         f"{variant[counter].get('last_name')}\n"
                                         f"Ссылка на профиль: https://vk.com/id"
                                         f"{variant[counter].get('id')}\n",
                                         attachment=','.join(attachment_photo))
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не понял вашего ответа...")


