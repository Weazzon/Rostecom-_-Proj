import pytest

from pages.auth import *
from pages.settings import *


@pytest.mark.auth
@pytest.mark.negative
@pytest.mark.parametrize('username', [fake_phone, fake_login, invalid_ls],
                         ids=['fake phone', 'fake login', 'fake account'])
def test_auth_page_fake_phone_login_account(browser, username):
    """Проверка авторизации по номеру телефона и паролю, лицевому счёту, неверный номер/логин/лс."""
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_pass_reg)
    time.sleep(30) # Время для ввода капчи при её появлении
    page.btn_click_enter()
    browser.implicitly_wait(5)

    error_message = browser.find_element(*AuthLocators.AUTH_FORM_ERROR)
    forgot_password = browser.find_element(*AuthLocators.AUTH_FORGOT_PASSWORD)

    assert error_message.text == 'Неверный логин или пароль' and \
        page.check_color(forgot_password) == '#ff4f12'


@pytest.mark.auth
@pytest.mark.negative
@pytest.mark.parametrize('username', [valid_phone, valid_email],
                         ids=['valid phone', 'valid_email'])
def test_auth_page_fake_password(browser, username):
    """Проверка авторизации по номеру телефона/почте/логину и паролю с использованием неверного пароля.
    Тестирование по номеру ЛС не проводится в связи с отсутствием реальных тестовых данных"""
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(fake_password)
    time.sleep(30) # Время для ввода капчи при её появлении
    page.btn_click_enter()
    browser.implicitly_wait(5)

    error_message = browser.find_element(*AuthLocators.AUTH_FORM_ERROR)
    forgot_password = browser.find_element(*AuthLocators.AUTH_FORGOT_PASSWORD)

    assert error_message.text == 'Неверный логин или пароль' and \
        page.check_color(forgot_password) == '#ff4f12'


@pytest.mark.auth
@pytest.mark.negative
@pytest.mark.parametrize('username', [1, 123456789], ids=['one digit', 'nine digits'])
def test_auth_page_invalid_phone_number(browser, username):
    """Проверка авторизации по номеру телефона с использованием неверного формата"""
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_pass_reg)
    page.btn_click_enter()
    browser.implicitly_wait(5)

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Неверный формат телефона'


@pytest.mark.auth
@pytest.mark.negative
def test_auth_page_username_blank_field(browser):
    """Проверка авторизации по номеру телефона/почте/логину/лицевому счёту - пустой строке"""
    page = AuthPage(browser)
    page.enter_username('')
    page.enter_password(valid_pass_reg)
    page.btn_click_enter()
    browser.implicitly_wait(5)

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Введите номер телефона' or \
        error_message.text == 'Введите адрес, указанный при регистрации' or \
        error_message.text == 'Введите логин, указанный при регистрации' or \
        error_message.text == 'Введите номер вашего лицевого счета'