import pytest

from pages.settings import *
from pages.auth import *
from pages.registration_email import RegistrationEmail


@pytest.mark.newpass
@pytest.mark.negative
def test_forgot_password_page(browser):
    """Проверка восстановления пароля по почте, негативные сценарии.
    ТРЕБУЕТСЯ РУЧНОЙ ВВОД КАПЧИ!"""
    sign_at = valid_email.find('@')
    mail_name = valid_email[0:sign_at]
    mail_domain = valid_email[sign_at + 1:len(valid_email)]

    page = NewPassPage(browser)
    page.enter_username(valid_email)
    time.sleep(30)  # Время для ввода капчи
    page.btn_click_continue()

    time.sleep(30)  # Ожидание письма с кодом

    # Проверяем почтовый ящик на наличие писем и получаем ID последнего письма
    result_id, status_id = RegistrationEmail().get_id_letter(mail_name, mail_domain)
    # Получаем id письма с кодом из почтового ящика
    letter_id = result_id[0].get('id')

    assert status_id == 200, 'status_id error'
    assert letter_id > 0, 'letter_id > 0 error'

    # Получаем код для восстановления пароля из письма от Ростелеком
    result_code, status_code = RegistrationEmail().get_reg_code(mail_name, mail_domain, str(letter_id))

    # Получаем body из текста письма
    text_body = result_code.get('body')
    # Извлекаем код из текста с помощью метода find
    reg_code = text_body[text_body.find('<b>') + len('<b>'):
                         text_body.find('<b>') + len('<b>') + 6]

    assert status_code == 200, 'status_code error'
    assert reg_code != '', 'reg_code != [] error'

    reg_digit = [int(char) for char in reg_code]
    print(reg_digit)
    browser.implicitly_wait(30)
    for i in range(0, 6):
        browser.find_elements(*NewPassLocators.NEWPASS_ONETIME_CODE)[i].send_keys(reg_code[i])
        browser.implicitly_wait(5)
    time.sleep(10)

    elem_new_pass = browser.find_element(*NewPassLocators.NEWPASS_NEW_PASS)
    elem_conf_pass = browser.find_element(*NewPassLocators.NEWPASS_NEW_PASS_CONFIRM)

    def input_new_pass(new_pass):
        browser.find_element(*NewPassLocators.NEWPASS_NEW_PASS).clear()
        elem_new_pass.send_keys(new_pass)
        time.sleep(5)
        browser.find_element(*NewPassLocators.NEWPASS_NEW_PASS_CONFIRM).clear()
        elem_conf_pass(new_pass)
        time.sleep(5)

    """Сценарий 1. Новый пароль менее 8 символов"""
    new_pass = valid_pass_reg[0:7]
    input_new_pass(new_pass)

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Длина пароля должна быть не менее 8 символов'

    """Сценарий 2. Новый пароль более 20 символов"""
    new_pass = valid_pass_reg[0:7]*3
    input_new_pass(new_pass)

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Длина пароля должна быть не более 20 символов'

    """Сценарий 3. Новый пароль не содержит заглавных букв"""
    new_pass = valid_pass_reg.lower()
    input_new_pass(new_pass)

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Пароль должен содержать хотя бы одну заглавную букву'

    """Сценарий 4. Новый пароль не содержит строчные буквы"""
    new_pass = valid_pass_reg.upper()
    input_new_pass(new_pass)

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Пароль должен содержать хотя бы одну прописную букву'

    """Сценарий 5. Новый пароль включает в себя букву на кириллице"""
    new_pass = f'{valid_pass_reg}{generate_string_ru(1)}'
    input_new_pass(new_pass)

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Пароль должен содержать только латинские буквы'

    """Сценарий 6. Новый пароль не содержит ни одной цифры или спецсимвола"""
    new_pass = valid_pass_reg
    for i in new_pass:
        if i.isdigit() or i in special_chars():
            new_pass = new_pass.replace(i, 'f')
        input_new_pass(new_pass)

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру'

    """Сценарий 7. Новый пароль отличается от пароля в поле 'Подтверждение пароля'."""
    browser.find_element(*NewPassLocators.NEWPASS_NEW_PASS).clear()
    new_pass = f'{valid_pass_reg[0:8]}{generate_string_en(2)}'
    elem_new_pass.send_keys(new_pass)
    time.sleep(3)

    browser.find_element(*NewPassLocators.NEWPASS_NEW_PASS_CONFIRM).clear()
    new_conf_pass = f'{valid_pass_reg[0:8]}{generate_string_en(4)}'
    elem_conf_pass.send_keys(new_conf_pass)
    time.sleep(3)

    browser.find_element(*NewPassLocators.NEWPASS_BTN_SAVE).click()

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Пароли не совпадают'

    """Сценарий 8. Новый пароль идентичен предыдущему"""
    new_pass = valid_pass_reg
    input_new_pass(new_pass)
    browser.find_element(*NewPassLocators.NEWPASS_BTN_SAVE).clicl()

    error_message = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_message.text == 'Этот пароль уже использовался, укажите другой пароль'