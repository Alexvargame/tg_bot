from aiogram import types

from email_validator import validate_email, EmailNotValidError


def vaild_email_filter(message: types.Message):
    try:
        email = validate_email(message.text)
    except EmailNotValidError:
        return None

    return {'email': email.normalized}

def vaild_email(text: str):
    try:
        email = validate_email(text)
    except EmailNotValidError:
        return None
    return email.normalized

# def valid_email_message_text(message:types.Message):
#     return vaild_email(message.text)
