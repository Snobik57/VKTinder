import pytest
import sqlalchemy as sq
from sqlalchemy_utils import database_exists, create_database, drop_database

from curse_project_VKTinder.tests.db_for_tests import DbVkTinder, Base, DSN


@pytest.fixture()
def setup():
    if not database_exists(sq.create_engine(DSN).url):
        create_database(sq.create_engine(DSN).url)
        Base.metadata.create_all(sq.create_engine(DSN))
    yield
    pass


@pytest.fixture()
def teardown():
    pass
    yield
    if database_exists(sq.create_engine(DSN).url):
        drop_database(sq.create_engine(DSN).url)


@pytest.fixture(scope="function", params=[
    (35819334, 'Тимур Гусев', 27, 2, 149, True),
    (12345678, 'Alex Pinkov', 32, 2, 156, True),
    (87654321, 'Serg Pronko', 23, 2, 165, True)])
def params_add_new_user(request):
    return request.param


def test_add_new_user(params_add_new_user, setup):
    (id_vk, name, age, sex, city, result) = params_add_new_user
    function_result = DbVkTinder().add_new_user(id_vk, name, age, sex, city)
    assert function_result == result
    assert isinstance(function_result, bool)


@pytest.fixture(scope="function", params=[
    (35819334, True),
    (12345678, True),
    (8761, False)])
def params_user_in_db(request):
    return request.param


def test_user_in_db(params_user_in_db):
    (id_vk, result) = params_user_in_db
    function_result = DbVkTinder().user_in_db(id_vk)
    assert function_result == result
    assert isinstance(function_result, bool)


@pytest.fixture(scope="function", params=[
    (35819334, 1),
    (12345678, 2),
    (87654321, 3)])
def params_get_id_user(request):
    return request.param


def test_get_id_user(params_get_id_user):
    (id_vk, result) = params_get_id_user
    function_result = DbVkTinder().get_id_user(id_vk)
    assert function_result == result
    assert isinstance(function_result, int)


@pytest.fixture(scope="function", params=[
    (35819334, 27),
    (12345678, 32),
    (87654321, 23)])
def params_get_age_user(request):
    return request.param


def test_get_age_user(params_get_age_user):
    (id_vk, result) = params_get_age_user
    function_result = DbVkTinder().get_age_user(id_vk)
    assert function_result == result
    assert isinstance(function_result, int)


@pytest.fixture(scope="function", params=[
    (35819334, 123, 'Serj Tankyan', 27, 2, 149, True),
    (12345678, 456, 'Robert Patison', 32, 2, 156, True),
    (87654321, 789, 'Filimonov Ser-gey', 23, 2, 165, True)])
def params_add_new_variants(request):
    return request.param


def test_add_new_variants(params_add_new_variants):
    (user_id_vk, variant_id_vk, name, age, sex, city, result) = params_add_new_variants
    function_result = DbVkTinder().add_new_variants(user_id_vk,
                                                    id_vk=variant_id_vk,
                                                    name=name,
                                                    age=age,
                                                    sex=sex,
                                                    city=city)
    assert function_result == result
    assert isinstance(function_result, bool)


@pytest.fixture(scope="function", params=[
    (35819334, 123, 'INERT', True),
    (12345678, 456, 'LIKE', True),
    (87654321, 789, 'DISLIKE', True)])
def params_new_status_for_variants(request):
    return request.param


def test_new_status_for_variants(params_new_status_for_variants):
    (user_id_vk, variant_id_vk, status, result) = params_new_status_for_variants
    function_result = DbVkTinder().new_status_for_variants(user_id_vk=user_id_vk,
                                                           variants_id=variant_id_vk,
                                                           status=status)
    assert function_result == result
    assert isinstance(function_result, bool)


@pytest.fixture(scope="function", params=[
    (35819334, 1),
    (12345678, 2),
    (87654321, 3)])
def params_count_new_variant(request):
    return request.param


def test_count_new_variant(params_count_new_variant):
    (id_vk, result) = params_count_new_variant
    function_result = DbVkTinder().count_new_variant(id_vk)
    assert function_result == result
    assert isinstance(function_result, int)


@pytest.fixture(scope="function", params=[
    (35819334, 'INERT', ['Serj Tankyan - https://vk.com/id123 ']),
    (12345678, 'INERT', ['Robert Patison - https://vk.com/id456 ']),
    (87654321, 'INERT', ['Filimonov Ser-gey - https://vk.com/id789 '])])
def params_get_all_variants_for_user(request):
    return request.param


def test_get_all_variants_for_user(params_get_all_variants_for_user):
    (id_vk, status, result) = params_get_all_variants_for_user
    function_result = DbVkTinder().get_all_variants_for_user(id_vk, status)
    assert function_result == result
    assert isinstance(function_result, list)


@pytest.fixture(scope="function", params=[
    (35819334, 123, True),
    (12345678, '456', False),
    (87654321, '456', False)])
def params_variant_in_db_for_user(request):
    return request.param


def test_variant_in_db_for_user(params_variant_in_db_for_user, teardown):
    (id_vk, id_vk_v, result) = params_variant_in_db_for_user
    function_result = DbVkTinder().variant_in_db_for_user(id_vk, id_vk_v)
    assert function_result == result
    assert isinstance(function_result, bool)
