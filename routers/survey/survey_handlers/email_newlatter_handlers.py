from aiogram import Router, types, F
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext

from routers.survey.states import Survey
from keyboards.command_keyboard import build_yes_or_no_kb


router = Router(name=__name__)

@router.message(Survey.email_newsletter, F.text.casefold() == 'yes')
async def handle_survey_email_newsletter_ok(message: types.Message, state:FSMContext):
    data = await state.update_data(newsletter_ok=True)
    await state.clear()
    await send_survey_results(message, data)


@router.message(Survey.email_newsletter, F.text.casefold() == 'no')
async def handle_survey_email_newsletter_not_ok(message: types.Message, state: FSMContext):
    data = await state.update_data(newsletter_ok=False)
    await state.clear()
    await send_survey_results(message, data)

@router.message(Survey.email_newsletter)
async def handle_survey_email_newsletter_could_not_understand(message: types.Message):
   await message.answer(
       text = (f"Sorry, I coun't understand,"
               f" please send {markdown.hcode('Yes')} or {markdown.hcode('No')}"
               ),
       reply_markup=build_yes_or_no_kb(),
   )

async def send_survey_results(message: types.Message, data: dict):
    text = markdown.text(
        'Your results:',
        "",
        markdown.text('Name:', markdown.hbold(data['full_name'])),
        markdown.text('Email:', markdown.hbold(data['email'])),
        markdown.text(
            "Preferred sport:", markdown.hbold(data['sport']),
        ),
        markdown.text(
            "Q:" ,markdown.hitalic(data['sport_question'])
        ),
        markdown.text(
            "A:", markdown.hitalic(data['sport_answer'])
        ),
        "",
        ("Will send you our news"
         if data['newsletter_ok']
         else "And won't bother you again"
         ),

        #message.text('Contact:', markdown.hbold(data['news_latter_ok'])),
        sep='\n',
    )
    await message.answer(
        text=text,
        reply_markup=types.ReplyKeyboardRemove()
    )

