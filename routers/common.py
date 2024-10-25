import asyncio
import logging

from aiogram import Router, types, F
from aiogram.enums import ChatAction
from aiogram.types import ReplyKeyboardRemove
from keyboards.command_keyboard import ButtonText
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


router = Router()

@router.message(F.text ==ButtonText.BYE)
async def handle_bye_message(message:types.Message):
    await message.answer(
        text="See you later! Click start any time",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(Command('cancel', prefix='!/'))
@router.message(F.text.casefold() == 'cancel')
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        await message.reply(text='Ok, but nothing was going on')
        return
    logging.info('Canceling state %r', current_state)
    await state.clear()
    await message.answer(
        'Canceled',
        reply_markup=ReplyKeyboardRemove()
    )

@router.message()
async def echo_message(message: types.Message):
    if message.poll:
        await message.forward(chat_id=message.chat.id)

        return
    await message.answer(
        text="Wait a second...",
        parse_mode=None,
    )
    if message.sticker:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.CHOOSE_STICKER,
        )

    try:
        await message.copy_to(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new 🙂")
