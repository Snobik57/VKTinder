import pytest
import requests

from curse_project_VKTinder.bot_func import write_msg, get_user_photos, get_user_info, user_search


def test_write_msg():
    assert isinstance(write_msg('35819334', 'hi'), int)
