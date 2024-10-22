import csv
import io

import aiohttp
from aiogram import Router, types
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.utils.chat_action import ChatActionSender
from keyboards.inline_keyboards.actions_kb import build_actions_kb

router = Router(name=__name__)


@router.message(Command("code"))
async def handle_command_code(message: types.Message):
    text = markdown.text(
        "Here's Python code:",
        "",
        markdown.markdown_decoration.pre_language(
            markdown.text
                ("print('Hello, world')",
                "\n",
                "def foo():\n    return 'bar'",
                sep="\n"),
            language="python",
        ),
        sep="\n",
    )
    await message.answer(text=text)


@router.message(Command("pic"))
async def handle_command_pic(message: types.Message):
    #url = 'https://img.freepik.com/free-photo/view-adorable-persian-domestic-cat_23-2151773881.jpg?semt=ais_hybrid'
    #file_path = 'https://img.freepik.com/free-photo/view-adorable-persian-domestic-cat_23-2151773881.jpg?semt=ais_hybrid'
    file_path = 'E:\Screenshot_15.png'
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    await message.reply_photo(
        photo=types.FSInputFile(
            path=file_path,
        ),
        caption='cat'
    )


@router.message(Command("file"))
async def handle_command_file(message: types.Message):
    file_path='E:\kassa.sqlite3'
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    await message.reply_document(
        document=types.FSInputFile(
            path=file_path,
            filename='doc.db'
        ),
    )


@router.message(Command('csv'))
async def send_scv_file(message: types.Message):
    file = io.StringIO()
    csv_writer = csv.writer(file)
    csv_writer.writerows([
        ['Name', 'Age', 'City'],
        ['John Smith', '28', 'New York'],
        ['Jane Doe', '32', 'Los Angeles'],
        ['Mike Johnson', '40', 'Chicago']
    ])
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue().encode('utf-8'),
            filename='people.csv'
        ),
    )


async def send_big_file(message:types.Message):
    url = 'https://img.freepik.com/free-photo/view-adorable-persian-domestic-cat_23-2151773881.jpg?semt=ais_hybrid'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as responce:
            result_bytes = await responce.read()
    await message.reply_document(
        document=types.BufferedInputFile(
            file=result_bytes,
            filename='cat_buff.jpg'
        )
    )


@router.message(Command('pic_file'))
async def send_pic_file_buffer(message:types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    async with action_sender:
        await send_big_file(message)


@router.message(Command("text"))
async def send_txt_file(message: types.Message):
    file = io.StringIO()
    file.write('Hello\n')
    file.write('A\n')
    await message.reply_document(
        document=types.BufferedInputFile(
          file=file.getvalue().encode('utf-8'),
          filename='text.txt'
        ),
    )

@router.message(Command("actions", prefix="!/"))
async def send_actions_message_w_kb(message: types.Message):
    await message.answer(
        text="Your actions:",
        reply_markup=build_actions_kb(),
    )