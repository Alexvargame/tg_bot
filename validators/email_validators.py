from aiogram import types

from email_validator import validate_email, EmailNotValidError


def vaild_email_filter(message: types.Message):
    try:
        email = validate_email(message.text)
    except EmailNotValidError:
        return None

    return {'email': email.normalized}