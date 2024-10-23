from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext

from .states import Survey
from validators.email_validators import vaild_email_filter
from keyboards.command_keyboard import build_yes_or_no_kb

router = Router(name=__name__)

@router.message(Command('survey', prefix="!/"))
async def handler_start_survey(message: types.Message, state: FSMContext):
    await state.set_state(Survey.full_name)
    await message.answer(
        text="Welcome to our weekly survey! What's your name?",
        reply_markup=types.ReplyKeyboardRemove(),
    )

@router.message(Survey.full_name, F.text)
async def handle_survey_user_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(Survey.email)
    # data = await state.get_data()
    # print(data)
    await message.answer(
        f"Hello, {markdown.hbold(message.text)}, now please share your email",
    )

@router.message(Survey.full_name)
async def handle_survey_user_full_name_invalid_content_type(message: types.Message):
    await message.answer(
        "Sorry, I didn't understand. send your full name as text",
    )

@router.message(Survey.email, vaild_email_filter)
async def handle_survey_user_email(message: types.Message, state: FSMContext, email:str):
    await state.update_data(email=email)
    await state.set_state(Survey.email_newslatter)
    await message.answer(
        text= f"Cool, your email is now {markdown.hcode(email)}. Would you like to be contacted in future?",
        reply_markup=build_yes_or_no_kb(),
    )


@router.message(Survey.email)
async def handle_survey_user_email_invalid_content_type(message: types.Message):
    await message.answer(
        "Sorry, I invalid email, please try again",
    )

async def send_survey_results(message: types.Message, data: dict):
    text = markdown.text(
        'Your results:',
        markdown.text('Name:', markdown.hbold(data['full_name'])),
        markdown.text('Email:', markdown.hbold(data['email'])),
        ("Will send you our news"
         if data['newslatter_ok']
         else "And won't bother you again"
         ),

        #message.text('Contact:', markdown.hbold(data['news_latter_ok'])),
        sep='\n',
    )
    await message.answer(
        text=text,
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.message(Survey.email_newslatter, F.text.casefold() == 'yes')
async def handle_survey_email_newslatter_ok(message: types.Message, state:FSMContext):
    data = await state.update_data(newslatter_ok=True)
    await state.clear()
    await send_survey_results(message, data)


@router.message(Survey.email_newslatter, F.text.casefold() == 'no')
async def handle_survey_email_newslatter_not_ok(message: types.Message, state: FSMContext):
    data = await state.update_data(newslatter_ok=False)
    await state.clear()
    await send_survey_results(message, data)

@router.message(Survey.email_newslatter)
async def handle_survey_email_newslatter_could_not_understand(message: types.Message):
   await message.answer(
       text = (f"Sorry, I coun't understand,"
               f" please send {markdown.hcode('Yes')} or {markdown.hcode('No')}"
               ),
       reply_markup=build_yes_or_no_kb(),
   )
