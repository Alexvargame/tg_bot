from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

class ButtonText:
    HELLO = "Hello"
    WHATS_NEXT = "What's next?"
    BYE = 'BYE'


def get_on_start_kb():
    button_hello = KeyboardButton(text=ButtonText.HELLO)
    button_help = KeyboardButton(text=ButtonText.WHATS_NEXT)
    button_bye = KeyboardButton(text=ButtonText.BYE)
    buttons_first_row = [button_hello, button_help]
    buttons_second_row = [button_bye]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_first_row, buttons_second_row],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup

def get_on_help_kb():
    numbers = [1,2,3,4,5,6,7,8,9,0]

    #buttons_row = [KeyboardButton(text=str(num)) for num in numbers]

    # markup = ReplyKeyboardMarkup(
    #     keyboard=[buttons_row],
    # )
    # return markup
    builder = ReplyKeyboardBuilder()
    for num in numbers:
        builder.button(text=str(num))
    builder.adjust(3, 3, 4)
    return builder.as_markup(resize_keyboard=True)

def get_action_kb():
    # markup = ReplyKeyboardMarkup(
    #     keyboard=[]
    # )
    # return markup
    builder = ReplyKeyboardBuilder()
    #builder.add(KeyboardButton(text="Send location", request_location=True))
    builder.button(text="Send location", request_location=True)
    builder.button(text="Send phone", request_contact=True)
    builder.button(text='Send pool', request_poll=KeyboardButtonPollType())
    builder.button(text='Send Quiz', request_poll=KeyboardButtonPollType(type='quiz'))
    builder.button(text='Dinner?', request_poll=KeyboardButtonPollType(type='regular'))
    builder.button(text=ButtonText.BYE)
    builder.adjust(1)
    return builder.as_markup(input_field_placeholder='Actions', resize_keyboard=True)

def build_yes_or_no_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Yes')
    builder.button(text='No')
    #builder.adjust(1)

    return builder.as_markup()