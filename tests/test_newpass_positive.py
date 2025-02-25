import pytest

from pages.auth import *
from pages.settings import *
from pages.registration_email import RegistrationEmail


@pytest.mark.skip(reason='при автотестировании не отправляется код на почту')
@pytest.mark.newpass
@pytest.mark.positive
def test_forgot_password_page(browser):
    """Проверка возможности восстановления пароля по почте.
    ТРЕБУЕТСЯ РУЧНОЙ ВВОД КАПЧИ!"""
    # Разделяем email на имя и домен для использования в следующих запросах
    sign_at = valid_email.find('@')
    mail_name = valid_email[0:sign_at]
    mail_domain = valid_email[sign_at + 1:len(valid_email)]

    page = NewPassPage(browser)
    page.enter_username(valid_email)
    time.sleep(40)  # Время для ввода капчи
    page.btn_click_continue()

    time.sleep(30)  # Ожидание получения письма на почту

    """Проверяем почтовый ящик на наличие писем и получаем ID последнего письма"""
    result_id, status_id = RegistrationEmail().get_id_letter(mail_name, mail_domain)
    # Получаем ID письма с кодом из почтового ящика
    letter_id = result_id[0].get('id')

    assert status_id == 200, 'status_id error'
    assert letter_id > 0, 'letter_id > 0 error'

    """Получаем код для восстановления пароля из письма от Ростелеком"""
    result_code, status_code = RegistrationEmail().get_reg_code(mail_name, mail_domain, str(letter_id))

    # Получаем body из текста письма
    text_body = result_code.get('body')
    # Извлекаем код из текста, используя метод find
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
    new_pass = fake_password
    browser.find_element(*NewPassLocators.NEWPASS_NEW_PASS).send_keys(new_pass)
    time.sleep(3)
    browser.find_element(*NewPassLocators.NEWPASS_NEW_PASS_CONFIRM).send_keys(new_pass)
    browser.find_element(*NewPassLocators.NEWPASS_BTN_SAVE).click()
    time.sleep(60)
    print(browser.current_url)

    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/authenticate'

    """В случае успешной смены пароля перезаписываем его в файл settings"""
    with open(r"../pages/settings.py", 'r', encoding='utf8') as file:
        lines = []
        for line in file.readlines():
            if 'valid_pass_reg' in line:
                lines.append(f"valid_pass_reg = '{fake_password}'\n")
            else:
                lines.append(line)
    with open(r"../pages/settings.py", 'w', encoding='utf8') as file:
        file.writelines(lines)