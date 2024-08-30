from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from exts.states import TwoQuestionsRouteStates
from exts.states import ChoiceRouteStates as States


router = Router()


@router.message(StateFilter(TwoQuestionsRouteStates.IsItIntellectualCase), F.text == "Нет")
async def start_route(msg: Message, state: FSMContext):
    await msg.answer("Cпор связан с банкротством?")
    await state.set_state(States.IsItCrash)
    await state.update_data({"isIntellectual": False})


@router.message(StateFilter(States.IsItCrash), F.text == "Да")  # TODO Арбитражный суд
async def is_it_crash_yes(msg: Message, state: FSMContext):
    await msg.answer("Чье банкротсвто рассматривается?")
    await state.set_state(States.WhoIsCrash)


@router.message(StateFilter(States.WhoIsCrash), F.text == "Физического лица")
async def Who_is_crash_FL(msg: Message, state: FSMContext):
    await msg.answer("укажите адрес места жительства должника")
    # TODO


@router.message(StateFilter(States.WhoIsCrash), F.text == "Юридического лица")
async def Who_is_crash_UL(msg: Message, state: FSMContext):
    await msg.answer("укажите адрес местонахождения ")
    # TODO


@router.message(StateFilter(States.IsItCrash), F.text == "Нет")
async def is_it_crash_no(msg: Message, state: FSMContext):
    await msg.answer("Спор связан с вашим статусом Юридического лица или индивидуального предпринимателя?")
    await state.set_state(States.AreYou_ULOrIP)


@router.message(StateFilter(States.AreYou_ULOrIP), F.text == "Что это?")
async def are_you_ul_or_ip_what_is_it(msg: Message, state: FSMContext):
    pass  # TODO сделать ответ


@router.message(StateFilter(States.AreYou_ULOrIP), F.text == "Да")
async def are_you_ul_or_ip_yes(msg: Message, state: FSMContext):
    await msg.answer("Связан ли спор с предпринимательской или иной экономической деятельностью")
    await state.set_state(States.IsItEconomicalCase)


@router.message(StateFilter(States.IsItEconomicalCase), F.text == "Да")
async def is_it_economical_case_yes(msg: Message, state: FSMContext):
    await msg.answer(
        "Ответчик является юридическим лицом, или спор связан с его статусом индивидуального предпринимателя?"
    )
    await state.set_state(States.IsYourDefendant_ULOrIP)


@router.message(StateFilter(States.IsYourDefendant_ULOrIP), F.text == "Нет")
async def is_your_defendant_ul_or_ip_no(msg: Message, state: FSMContext):
    await msg.answer("Спор связан с оспариванием действий государственных органов?")
    await state.set_state(States.IsYourDefendentCountry)


@router.message(StateFilter(States.IsYourDefendentCountry), F.text == "Да")  # TODO Арбитражный суд
async def is_your_defendant_country_yes(msg: Message, state: FSMContext):
    await msg.answer("Вы спорите с арбитражным судом? (Просим одуматься)")
    await state.set_state(States.IsYourDefendentArbitrationCourt)


@router.message(StateFilter(States.IsYourDefendentArbitrationCourt), F.text == "Да")
async def is_your_defendant_arbitration_court_yes(msg: Message, state: FSMContext):
    await msg.answer("Вы спорите с арбитражным судом? (Просим одуматься)")
    await state.set_state(States.IsItMoscowArbitrationCourt)


@router.message(StateFilter(States.IsItMoscowArbitrationCourt), F.text == "Да")
async def is_it_moscow_arbitration_court_yes(msg: Message, state: FSMContext):
    await msg.answer("Арбитражный суд Тверской области")
    await state.set_state(None)


@router.message(StateFilter(States.IsItMoscowArbitrationCourt), F.text == "Нет")
async def is_it_moscow_arbitration_court_no(msg: Message, state: FSMContext):
    await msg.answer("Арбитражный суд Московской области")
    await state.set_state(None)


@router.message(StateFilter(States.IsYourDefendentArbitrationCourt), F.text == "Нет")
async def is_your_defendant_arbitration_court_no(msg: Message, state: FSMContext):
    await msg.answer("Оспариваются действия федеральной службы судебных приставов")
    await state.set_state(States.IsIt_FSSP)


@router.message(StateFilter(States.IsIt_FSSP), F.text == "Да")  # TODO Сделать обработку адреса
async def is_it_fssp_yes(msg: Message, state: FSMContext):
    await msg.answer("Укажите адрес судебного пристава-исполнителя")
    await state.set_state(None)


@router.message(StateFilter(States.IsIt_FSSP), F.text == "Нет")
async def is_it_fssp_no(msg: Message, state: FSMContext):
    await msg.answer("Спор связан с недвижимым имуществом?")
    await state.set_state(States.IsItRealtyCase)


@router.message(StateFilter(States.IsItRealtyCase), F.text == "Да")  # TODO Сделать обработку адреса
async def is_it_realty_case_yes(msg: Message, state: FSMContext):
    await msg.answer("Укажите адрес имущества")
    await state.set_state(None)


@router.message(StateFilter(States.IsItRealtyCase), F.text == "Нет")
async def is_it_realty_case_no(msg: Message, state: FSMContext):
    await msg.answer("Спор с правами на морские и воздушные суда, суда внутреннего плавания, космические объекты?")
    await state.set_state(States.IsItSpace)


@router.message(StateFilter(States.IsItSpace), F.text == "Да")  # TODO Сделать обработку адреса
async def is_it_space_yes(msg: Message, state: FSMContext):
    await msg.answer("Укажите адрес регистрации имущества")
    await state.set_state(None)


@router.message(StateFilter(States.IsItSpace), F.text == "Нет")  # TODO Сделать обработку адреса
async def is_it_space_no(msg: Message, state: FSMContext):
    await msg.answer("Укажите адрес ответчика")
    await state.set_state(None)
