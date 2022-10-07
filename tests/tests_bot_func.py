import pytest

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from curse_project_VKTinder.bot_func import write_msg, get_user_photos, get_user_info, user_search, vk


keyboard_test = VkKeyboard(one_time=True)
keyboard_test.add_button("TEST", VkKeyboardColor.POSITIVE)
fixture_write_msg = [
    (35819334, 'test_string', 'photo35819334_457240247', keyboard_test, True)
]


@pytest.mark.parametrize('user_id, test_string, photo_string, keyboard, right_result', fixture_write_msg)
def test_write_msg(user_id, test_string, photo_string, keyboard, right_result):
    function_result = write_msg(user_id, test_string, photo_string, keyboard)
    params = {
        'message_ids': function_result.get('id_msg'),
        'delete_for_all': 1
    }
    vk.method('messages.delete', params)
    assert isinstance(function_result, dict)
    assert right_result == function_result.get('result')


fixture_get_user_photos = [
    (35819334, ([{'like': 42,
                  'photo_id': 436290356,
                  'photo_url': 'https://sun9-88.userapi.com/impf/c636419/v636419334/2932b/WoaqPbbrryM.jpg?size=130x130&'
                               'quality=96&sign=ea072130fde2cd111c26ab331e4666e6&c_uniq_tag=un7wHkAGw7k1wXgtRVSjcccEmxy'
                               'S0FaG766Z2eu-300&type=album'},
                 {'like': 32,
                  'photo_id': 456239926,
                  'photo_url': 'https://sun9-57.userapi.com/impf/c849216/v849216147/13740f/EjuCHClXYk8.jpg?size=130x87&'
                               'quality=96&sign=edbe9a405b061f48353302606c8f4247&c_uniq_tag=BfZ7ICX7QjGCNuX8zLhDG9WQ4xq'
                               'RLiOilQEMb3PykOI&type=album'},
                 {'like': 14,
                  'photo_id': 456239468,
                  'photo_url': 'https://sun9-87.userapi.com/impf/c841332/v841332060/71850/mgKw1D9Yn5U.jpg?size=97x130&q'
                               'uality=96&sign=53eba3451e73806acb27fdec6aecaa76&c_uniq_tag=CZuMF5QF8s-HhhhL1r3mM9wOTkN'
                               '7MtBtLE2g2ZZeZsE&type=album'}]))
]


@pytest.mark.parametrize('user_id, result', fixture_get_user_photos)
def test_get_user_photos(user_id, result):
    function_result = get_user_photos(user_id)
    assert isinstance(function_result, list)
    assert result == function_result


fixture_get_user_info = [
    (35819334, {'city': 149, 'first_name': 'Тимур', 'gender': 2, 'last_name': 'Гусев'}),
    (2736397, {'city': 99, 'first_name': 'Антон', 'gender': 2, 'last_name': 'Чернов'}),
    (449190194, {'city': None, 'first_name': 'Василий', 'gender': 2, 'last_name': 'Крашенинников'})
]


@pytest.mark.parametrize('user_id, result', fixture_get_user_info)
def test_get_user_info(user_id, result):
    function_result = get_user_info(user_id)
    assert isinstance(function_result, dict)
    assert result == function_result


fixture_user_search = [
    (35819334, 25, 29, 409),
    (2736397, 30, 34, 316),
    (449190194, 40, 44, 324)
]


@pytest.mark.parametrize('user_id, age_from, age_to, len_result', fixture_user_search)
def test_user_search(user_id, age_from, age_to, len_result):
    function_result = user_search(user_id, age_from=age_from, age_to=age_to)
    assert isinstance(function_result, dict)
    assert isinstance(function_result.get('count'), int)

