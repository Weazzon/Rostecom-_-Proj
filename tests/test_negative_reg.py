import pytest

from pages.settings import *
from pages.auth import *


@pytest.mark.reg
@pytest.mark.negative
@pytest.mark.parametrize('firstname', ['', generate_string_ru(1), generate_string_ru(31), generate_string_ru(256),
                                       en_chars(), chinese_chars(), special_chars(), 12345],
                         ids=['empty', 'one char', '31 chars', '256 chars',
                              'english chars', 'chinese', 'special', 'number'])
def test_registration_with_invalid_firstname(browser, firstname):
    """Негативные тесты регистрации на сайте. Невалидный формат имени"""
    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(3)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

    page = RegPage(browser)
    page.enter_firstname(firstname)
    browser.implicitly_wait(3)
    page.enter_lastname(fake_lastname)
    browser.implicitly_wait(3)
    page.enter_email(fake_email)
    browser.implicitly_wait(3)
    page.enter_password(fake_password)
    browser.implicitly_wait(3)
    page.enter_pass_conf(fake_password)
    browser.implicitly_wait(3)
    page.btn_click()

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'


@pytest.mark.reg
@pytest.mark.negative
@pytest.mark.parametrize('lastname', ['', generate_string_ru(1), generate_string_ru(31),
                                      generate_string_ru(256), en_chars(), chinese_chars(), special_chars(), 12345],
                         ids=['empty', 'one char', '31 chars', '256 chars', 'english chars',
                              'chinese', 'special', 'number'])
def test_registration_with_invalid_lastname(browser, lastname):
    """Невалидный формат фамилии"""
    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(3)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

    page = RegPage(browser)
    page.enter_firstname(fake_firstname)
    browser.implicitly_wait(3)
    page.enter_lastname(lastname)
    browser.implicitly_wait(3)
    page.enter_email(fake_email)
    browser.implicitly_wait(3)
    page.enter_password(fake_password)
    browser.implicitly_wait(3)
    page.enter_pass_conf(fake_password)
    browser.implicitly_wait(3)
    page.btn_click()

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'


@pytest.mark.reg
@pytest.mark.negative
@pytest.mark.parametrize('phone', ['', 1, 123456789, generate_string_ru(10), special_chars()],
                         ids=['empty', 'one digit', '9 digits', 'string', 'special chars'])
def test_registration_with_invalid_phone_format(browser, phone):
    """Невалидный формат номера телефона"""
    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(3)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

    page = RegPage(browser)
    page.enter_firstname(fake_firstname)
    browser.implicitly_wait(3)
    page.enter_lastname(fake_lastname)
    browser.implicitly_wait(3)
    page.enter_email(phone)
    browser.implicitly_wait(3)
    page.enter_password(fake_password)
    browser.implicitly_wait(3)
    page.enter_pass_conf(fake_password)
    browser.implicitly_wait(3)
    page.btn_click()

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, ' \
                                 'или email в формате example@email.ru'


@pytest.mark.reg
@pytest.mark.negative
@pytest.mark.parametrize('email', ['', '@', '@.', '.', generate_string_ru(20), f'{rus_chars()}@mail.ru',
                                   f'{chinese_chars()}@mail.ru', 1234567],
                         ids=['empty', 'at', 'at dot', 'dot', 'string', 'russian', 'chinese', 'numbers'])
def test_registration_with_invalid_email_format(browser, email):
    """Невалидный формат электронной почты"""
    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(3)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

    page = RegPage(browser)
    page.enter_firstname(fake_firstname)
    browser.implicitly_wait(3)
    page.enter_lastname(fake_lastname)
    browser.implicitly_wait(3)
    page.enter_email(email)
    browser.implicitly_wait(3)
    page.enter_password(fake_password)
    browser.implicitly_wait(3)
    page.enter_pass_conf(fake_password)
    browser.implicitly_wait(3)
    page.btn_click()

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, ' \
                                 'или email в формате example@email.ru'


@pytest.mark.reg
@pytest.mark.negative
def test_registration_password_differs_pass_confirmation(browser):
    """Данные в поле 'Пароль' и 'Подтверждение пароля' не совпадают"""
    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(3)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

    page = RegPage(browser)
    page.enter_firstname(fake_firstname)
    browser.implicitly_wait(3)
    page.enter_lastname(fake_lastname)
    browser.implicitly_wait(3)
    page.enter_email(fake_email)
    browser.implicitly_wait(3)
    page.enter_password(fake_password)
    browser.implicitly_wait(3)
    page.enter_pass_conf(valid_pass_reg)
    browser.implicitly_wait(3)
    page.btn_click()

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Пароли не совпадают'