from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from main import dp

router = Router()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    #{markdown.hide_link()}
    await message.answer(text=f"Hello. {markdown.hbold(message.from_user.full_name)}", parse_mode='html')


@dp.message(Command('help'))
async def handle_help(message: types.Message):
    text = markdown.text(
            markdown.markdown_decoration.quote("I'm and {echo} bot."),
                    markdown.text("Send me",
                                  markdown.markdown_decoration.bold(
                                      markdown.text(
                                  markdown.underline('literally'),
                                            "any",
                                      ),
                                  ),
                                  markdown.markdown_decoration.quote("message!"),
                    sep="\n",
            )
    )
    await message.answer(text=text, parse_mode=ParseMode.HTML)#ParseMode.MARKDOWN_V2)
