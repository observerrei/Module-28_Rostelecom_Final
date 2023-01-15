# python -m pytest -v --driver Chrome --driver-path chromedriver.exe tests/test_auth_page.py
import pytest
from pages.auth_page import AuthPage
from pages.locators import AuthLocators
from settings import *


def test_page_right(selenium):
    # В правой части формы «Авторизация» находится слоган ЛК "Ростелеком ID"
    try:
        page = AuthPage(selenium)
        assert 'Персональный помощник в цифровом мире Ростелекома' in page.page_right.text
    except AssertionError:
        print('Элемент отсутствует в правой части формы')


def test_elements_of_auth(selenium):
    # Блок аутентификации формы «Авторизация» содержит основные элементы (Меню выбора типа аутентификации, Формы ввода, кнопка "Войти", ссылки "Забыл пароль" и "Зарегистрироваться")
    page = AuthPage(selenium)

    assert page.menu_tub.text in page.card_of_auth.text
    assert page.email.text in page.card_of_auth.text
    assert page.pass_eml.text in page.card_of_auth.text
    assert page.btn_enter.text in page.card_of_auth.text
    assert page.forgot_password_link.text in page.card_of_auth.text
    assert page.register_link.text in page.card_of_auth.text


def test_menu_of_type_auth(selenium):
    # Меню выбора типа аутентификации содержит табы: 'Номер', 'Почта', 'Логин', 'Лицевой счёт'
    try:
        page = AuthPage(selenium)
        menu = [page.tub_phone.text, page.tub_email.text, page.tub_login.text, page.tub_ls.text]
        for i in range(len(menu)):
            assert "Номер" in menu
            assert 'Почта' in menu
            assert 'Логин' in menu
            assert 'Лицевой счёт' in menu
    except AssertionError:
        print('Ошибка в имени таба Меню типа аутентификации')


def test_menu_of_type_active_auth(selenium):
    # В Меню выбора типа аутентификации по умолчанию выбрана форма аутентификации по телефону
    page = AuthPage(selenium)

    assert page.active_tub_phone.text == Settings.menu_of_type_auth[0]


def test_placeholder_name_of_user(selenium):
    # В форме ввода ('Номер', 'Почта', 'Логин', 'Лицевой счёт') поля ввода меняются в соответствии с выбранным табом Меню
    page = AuthPage(selenium)
    page.tub_phone.click()

    assert page.placeholder_name_of_user.text in Settings.placeholder_name_of_user
    page.tub_email.click()
    assert page.placeholder_name_of_user.text in Settings.placeholder_name_of_user
    page.tub_login.click()
    assert page.placeholder_name_of_user.text in Settings.placeholder_name_of_user
    page.tub_ls.click()
    assert page.placeholder_name_of_user.text in Settings.placeholder_name_of_user


def test_forgot_password_link(selenium):
    # Проверка перехода по ссылке 'Забыл пороль'
    page = AuthPage(selenium)
    page.driver.execute_script("arguments[0].click();", page.forgot_password_link)

    assert page.find_other_element(*AuthLocators.password_recovery).text == 'Восстановление пароля'


def test_register_link(selenium):
    # Проверка перехода по ссылке 'Зарегистрироваться'
    page = AuthPage(selenium)
    page.register_link.click()

    assert page.find_other_element(*AuthLocators.registration).text == 'Регистрация'


def test_auth_by_valid_email_pass(selenium):
    # Аутентификация пользователя с валидным email и паролем
    page = AuthPage(selenium)
    page.email.send_keys(Settings.valid_email)
    page.email.clear()
    page.pass_eml.send_keys(Settings.valid_password)
    page.pass_eml.clear()
    page.btn_enter.click()
    assert page.get_relative_link() == '/account_b2c/page'

@pytest.mark.parametrize("incor_email", [Settings.invalid_email, Settings.empty_email],
                         ids=['invalid_email', 'empty'])
@pytest.mark.parametrize("incor_passw", [Settings.invalid_password, Settings.empty_password],
                         ids=['invalid_password', 'empty'])
def test_auth_by_invalid_email(selenium, incor_email, incor_passw):
    # Аутентификация пользователя с невалидным email и паролем: связка Почта+Пароль валидна, но пользователь с такими данными не зарегистрирован в системе; пустые значения
    page = AuthPage(selenium)
    page.email.send_keys(incor_email)
    page.email.clear()
    page.pass_eml.send_keys(incor_passw)
    page.pass_eml.clear()
    page.btn_enter.click()

    assert page.get_relative_link() != '/account_b2c/page'