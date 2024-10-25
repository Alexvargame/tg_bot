import logging

from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state, default_state

from .states import Survey, SurveySportDetail

from .survey_handlers.email_newlatter_handlers import router as email_newsletter_router
from .survey_handlers.user_email_handlers import router as user_email_router
from .survey_handlers.full_name import router as full_name_router
from .survey_handlers.select_sport_handlers import router as select_sport_router

router = Router(name=__name__)
router.include_routers(
    email_newsletter_router,
    select_sport_router,
    user_email_router,
    full_name_router,

)

@router.message(Command('survey', prefix="!/"), default_state)
async def handler_start_survey(message: types.Message, state: FSMContext):
    await state.set_state(Survey.full_name)
    await message.answer(
        text="Welcome to our weekly survey! What's your name?",
        reply_markup=types.ReplyKeyboardRemove(),
    )

survey_states = StateFilter(Survey(), SurveySportDetail())
@router.message(Command('cancel', prefix='!/'), survey_states)
@router.message(F.text.casefold() == 'cancel', survey_states)
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()

    logging.info('Canceling state %r', current_state)
    await state.clear()
    await message.answer(
        f'Canceled survey on step {current_state}. Start again.',
        reply_markup=types.ReplyKeyboardRemove()
    )
