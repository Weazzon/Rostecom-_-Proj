import pytest

from pages.auth import *
from pages.settings import *
from pages.registration_email import RegistrationEmail


class TestRegistration:
    result_email, status_email = RegistrationEmail().get_api_email()  # Запрос на получение почтового ящика
    email_reg = result_email[0]

    @pytest.mark.reg
    @pytest.mark.positive
    def test_registration_positive(self, browser):
        """При тестировании используется сервис '1secmail.com'. Сервис имеет открытый API"""

        # Для использования в будущих запросах разделим email на имя и домен
        at_sign = self.email_reg.find('@')
        mail_name = self.email_reg[0:at_sign]
        mail_domain = self.email_reg[at_sign + 1:len(self.email_reg)]
        assert self.status_email == 200, 'status_email error'
        assert len(self.result_email) > 0, 'len(result_email) > 0 error'

        page = AuthPage(browser)
        page.enter_reg_page()
        browser.implicitly_wait(3)
        assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

        page = RegPage(browser)
        page.enter_firstname(fake_firstname)
        browser.implicitly_wait(3)
        page.enter_lastname(fake_lastname)
        browser.implicitly_wait(3)
        page.enter_email(self.email_reg)
        browser.implicitly_wait(3)
        page.enter_password(fake_password)
        browser.implicitly_wait(3)
        page.enter_pass_conf(fake_password)
        browser.implicitly_wait(3)
        page.btn_click()
        time.sleep(30)  # Время для ожидания письма

        result_id, status_id = RegistrationEmail().get_id_letter(mail_name, mail_domain)
        letter_id = result_id[0].get('id')
        assert status_id == 200, 'status_id error'
        assert letter_id > 0, 'letter_id > 0 error'

        # Получаем код регистрации из письма от Ростелеком
        result_code, status_code = RegistrationEmail().get_reg_code(mail_name, mail_domain, str(letter_id))

        # Получаем body из текста письма и извлекаем код регистрации
        text_body = result_code.get('body')
        reg_code = text_body[text_body.find('<b>') + len('<b>'):
                             text_body.find('<b>') + len('<b>') + 6]
        assert status_code == 200, 'status_code error'
        assert reg_code != '', 'reg_code != [] error'

        reg_digit = [int(char) for char in reg_code]
        print(reg_digit)
        browser.implicitly_wait(20)
        for i in range(0, 6):
            browser.find_elements(By.XPATH, '//input[@inputmode="numeric"]')[i].send_keys(reg_code[i])
            browser.implicitly_wait(5)
        browser.implicitly_wait(20)

        # Проверяем, что регистрация пройдена и пользователь перенаправлен в личный кабинет
        assert page.get_relative_link() == '/account_b2c/page', 'Регистрация не пройдена'
        page.driver.save_screenshot('reg_complete.png')

        # В случае успешной регистрации перезаписываем созданную пару email/пароль в файл settings
        print(self.email_reg, fake_password)
        with open(r"../pages/settings.py", 'r', encoding='utf8') as file:
            lines = []
            print(lines)
            for line in file.readlines():
                if 'valid_email' in line:
                    lines.append(f"valid_email = '{str(self.email_reg)}'\n")
                elif 'valid_pass_reg' in line:
                    lines.append(f"valid_pass_reg = '{fake_password}'\n")
                else:
                    lines.append(line)
        with open(r"../pages/settings.py", 'w', encoding='utf8') as file:
            file.writelines(lines)