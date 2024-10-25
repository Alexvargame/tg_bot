from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown
from keyboards.command_keyboard import build_yes_or_no_kb
from routers.survey.states import Survey, KnownSports

from keyboards.command_keyboard import build_select_kb

router = Router(name=__name__)

from email_validator import validate_email

@router.message(Survey.email,
                #vaild_email_filter,
                #F.func(valid_email_message_text).as_('email'),
                #F.text.cast(vaild_email).as_('email'),
                F.text.cast(validate_email).normalized.as_('email'),
                )
async def handle_survey_user_email(message: types.Message, state: FSMContext, email:str):
    await state.update_data(email=email)
    await state.set_state(Survey.sport)
    await message.answer(
        text= f"Cool, your email is now {markdown.hcode(email)}."
              f"What is your favorite sport?",
        reply_markup=build_select_kb(KnownSports),
    )


@router.message(Survey.email)
async def handle_survey_user_email_invalid_content_type(message: types.Message):
    await message.answer(
        "Sorry, I invalid email, please try again. Cancel survey? Tap '/cancel'",
    )
