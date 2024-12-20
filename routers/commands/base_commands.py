from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from keyboards.command_keyboard import ButtonText, get_on_start_kb
from keyboards.inline_keyboards.info_kb import build_info_kb

router = Router(name=__name__)

from keyboards.command_keyboard import (
    get_on_start_kb,
    get_on_help_kb,
    get_action_kb,
    ButtonText
)
@router.message(CommandStart())
async def handle_start(message: types.Message):

    url = "https://w7.pngwing.com/pngs/547/380/png-transparent-robot-waving-hand-bot-ai-robot-thumbnail.png"

    await message.answer(
        text=f"{markdown.hide_link(url)}Hello, {markdown.hbold(message.from_user.full_name)}!",
        parse_mode=ParseMode.HTML,
        reply_markup=get_on_start_kb(),
    )
    #await message.answer(text=f"Hello. {markdown.hbold(message.from_user.full_name)}", parse_mode='html')



@router.message(F.text == ButtonText.WHATS_NEXT)
@router.message(Command('help'))
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
    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_on_help_kb(),
    )

@router.message(Command('more', prefix="!/more"))
async def handler_more(message:types.Message):
    await message.answer(
        text="Choose action",
        reply_markup=get_action_kb()
    )



@router.message(Command('info', prefix="!/info"))
async def handler_info_command(message:types.Message):
    await message.answer(
        text="Links and other:",
        reply_markup=build_info_kb()
    )


