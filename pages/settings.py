"""Данные для авторизации в системе"""
import os
from dotenv import load_dotenv
from faker import Faker
import string
load_dotenv()


"""Фальшивые данные для авторизации в системе"""
fake_ru = Faker('ru_RU')
fake_firstname = fake_ru.first_name()
fake_lastname = fake_ru.last_name()
fake_phone = fake_ru.phone_number()
fake = Faker()
fake_password = fake.password()
fake_login = fake.user_name()
fake_email = fake.email()

valid_phone = os.getenv('PHONE')
valid_login = os.getenv('LOGIN')
valid_password = os.getenv('PASSWORD')
invalid_ls = '387649004455'

valid_email = 'auvxn5j2r1@txcct.com'
valid_pass_reg = 'kek+#vekR'


def generate_string_ru(n):
    return 'ы' * n


def generate_string_en(n):
    return 's' * n


def en_chars():
    return 'abcdefghijklmnopqrstuvwxyz'


def rus_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():  # 10 самых популярных китайских иероглифов
    return '的一是不了在人有我他'


def special_chars():
    return f'{string.punctuation}'