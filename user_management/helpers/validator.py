import re

from django.contrib.auth.models import User


def is_fields_filled(*fields):
    for field in fields:
        if field == '':
            return False
    return True


def is_correct_email(email):
    return re.match('[A-Za-z0-9-_]+@[a-z]{1,9}\.[a-z]{2,5}', email)


def is_email_free(email):
    return not User.objects.filter(username=email).exists()


def is_correct_password(password):
    return re.match('[A-Za-z0-9-_]{6,30}', password)


def is_passwords_match(password, confirm_password):
    return password == confirm_password


def is_correct_name(*name_parts):
    for name_part in name_parts:
        if not re.match('[A-Za-zА-Яа-я]{1,25}',name_part):
            return False
    return True



