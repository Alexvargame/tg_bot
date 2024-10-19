import asyncio
import csv
import logging
import io
import aiohttp


from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums import ChatAction
from config import settings


bot = Bot(token=settings.bot_token)
dp = Dispatcher()


@dp.message(Command("code"))
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

# async def is_photo(message: types.Message):
#     return message.photo

@dp.message(Command("pic"))
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

@dp.message(Command("file"))
async def handle_command_pic(message: types.Message):
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

@dp.message(Command('csv'))
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

@dp.message(Command('pic_file'))
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
    # url = 'https://img.freepik.com/free-photo/view-adorable-persian-domestic-cat_23-2151773881.jpg?semt=ais_hybrid'
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as responce:
    #         result_bytes = await responce.read()
    # await message.reply_document(
    #     document=types.BufferedInputFile(
    #         file=result_bytes,
    #         filename='cat_buff.jpg'
    #     )
    # )

@dp.message(Command("text"))
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
#@dp.message(lambda message: message.photo)
@dp.message(F.photo, ~F.caption)
async def handle_photo_wo_caption(message: types.Message):
    caption = "Can't see, sorry"
    # await message.bot.send_photo(
    #     chat_id=message.chat.id
    # )
    await message.reply_photo(
        photo=message.photo[-1].file_id,
        caption=caption
    )

@dp.message(F.photo, F.caption.contains("please"))
async def handle_photo_with_please_caption(message: types.Message):
    await message.reply("Can't see")

any_media_filter = F.photo | F.video | F.document

@dp.message(any_media_filter, ~F.caption)
async def handle_any_media_wo_caption(message: types.Message):
    if message.document:
        await message.reply_document(
            document=message.document.file_id,
        )
    elif message.video:
        await message.reply_video(
            video=message.video.file_id
        )
    else:
        await message.reply("I can't see any media")


@dp.message()
async def echo_message(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text='Start...'

    )
    await bot.send_message(
        chat_id=message.chat.id,
        text='Detecting message ...',
        reply_to_message_id=message.message_id
    )
    await message.answer('Wait a second...',
                         parse_mode=None)
    # if message.text:
    #     await message.answer(
    #         text=message.text,
    #         entities=message.entities
    #     )
    if message.sticker:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.CHOOSE_STICKER,
        )
        await asyncio.sleep(2)
    try:
        await message.copy-to(
            chat_id=message.chat.id
        )
        #await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Something')

    # if message.text:
    #     await message.reply(text=message.text)
    # elif message.sticker:
    #     await bot.send_sticker(
    #         chat_id=message.chat.id,
    #         sticker=message.sticker.file_id
    #     )
    #     #await message.reply_sticker(sticker=message.sticker.file_id)
    # else:
    #     await message.reply(text='Something')

async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
