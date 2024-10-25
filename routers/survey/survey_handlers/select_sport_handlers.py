from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.utils import markdown
from routers.survey.states import Survey, KnownSports, SurveySportDetail, KnownF1Tracks

from keyboards.command_keyboard import build_select_kb, build_yes_or_no_kb

router = Router(name=__name__)

known_sport_to_next: dict[KnownSports, tuple[State, str]] = {
    KnownSports.tennis:(
        SurveySportDetail.tennis,
        "Who is your favorite tennis player",
    ),
    KnownSports.football:(
        SurveySportDetail.football,
        'What is your favorite team?'
    ),
    KnownSports.formula_one:(
        SurveySportDetail.formula_one,
        'What is your favorite track?'
    ),
}

known_f1_tracks_kb = build_select_kb(KnownF1Tracks)
known_sport_kb: dict={
    KnownSports.formula_one: known_f1_tracks_kb
}
@router.message(
    Survey.sport,
    F.text.cast(KnownSports),
)
async def select_sport(message: types.Message, state:FSMContext):
    next_state, question_text = known_sport_to_next[message.text]
    await state.update_data(sport=message.text, sport_question=question_text)
    await state.set_state(next_state)
    kb = types.ReplyKeyboardRemove()
    if message.text in known_sport_kb:
        kb = known_sport_kb[message.text]
    await message.answer(
        text=question_text,
        reply_markup=kb
    )

@router.message(Survey.sport)
async def select_sport_invalid_choice(message: types.Message):
    await message.answer(
        'Unknown sport. Please select one of the following:',
        reply_markup=build_select_kb(KnownSports)
    )

@router.message(F.text, StateFilter(SurveySportDetail.football, SurveySportDetail.tennis))
@router.message(F.text.cast(KnownF1Tracks), SurveySportDetail.formula_one)
async def handle_select_sport_details_option(message:types.Message, state: FSMContext):
    await state.update_data(sport_answer=message.text)
    await state.set_state(Survey.email_newsletter)
    await message.answer(
        text='Would you like to be notified about this sport? Email newlatter',
        reply_markup=build_yes_or_no_kb()
    )

@router.message(SurveySportDetail.tennis)
async def handle_tennis_player_not_text(message:types.Message):
    await message.answer(
        text='Please name tennis player using text'
    )

@router.message(SurveySportDetail.football)
async def handle_football_team_not_text(message:types.Message):
    await message.answer(
        text='Please name football team using text'
    )

@router.message(SurveySportDetail.formula_one)
async def handle_formula_one_not_one_of_tracks(message:types.Message):
    await message.answer(
        text='Please choise track',
        reply_markup=known_f1_tracks_kb,

    )
