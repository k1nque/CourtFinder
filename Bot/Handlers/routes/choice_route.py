from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from exts.states import TwoQuestionsRouteStates, IntellectualRouteStates
from exts.states import ChoiceRouteStates as States

from Keyboards.keyboards_markups import choice_kb


router = Router()


@router.message(StateFilter(TwoQuestionsRouteStates.IsItIntellectualCase), F.text == "Нет")
@router.message(StateFilter(IntellectualRouteStates.Copyright), F.text == "Да")
@router.message(StateFilter(IntellectualRouteStates.FOIP), F.text == "Нет")
@router.message(StateFilter(IntellectualRouteStates.Rospatent), F.text == "Нет")
async def start_route(msg: Message, state: FSMContext):
    await state.set_state(States.IsItCrash)
    await state.update_data({"isIntellectual": False})
    return await msg.answer("Cпор связан с банкротством?")


@router.message(StateFilter(States.IsItCrash), F.text == "Да")  # TODO Арбитражный суд
async def is_it_crash_yes(msg: Message, state: FSMContext):
    await state.set_state(States.WhoIsCrash)
    return await msg.answer("Чье банкротсвто рассматривается?", reply_markup=choice_kb)


@router.message(StateFilter(States.WhoIsCrash), F.text == "Физического лица")
async def Who_is_crash_FL(msg: Message, state: FSMContext):
    # TODO
    return await msg.answer("укажите адрес места жительства должника")


@router.message(StateFilter(States.WhoIsCrash), F.text == "Юридического лица")
async def Who_is_crash_UL(msg: Message, state: FSMContext):
    # TODO
    return await msg.answer("укажите адрес местонахождения ")


@router.message(StateFilter(States.IsItCrash), F.text == "Нет")
async def is_it_crash_no(msg: Message, state: FSMContext):
    await state.set_state(States.AreYou_ULOrIP)
    return await msg.answer("Спор связан с вашим статусом Юридического лица или индивидуального предпринимателя?")


@router.message(StateFilter(States.AreYou_ULOrIP), F.text == "Что это?")
async def are_you_ul_or_ip_what_is_it(msg: Message, state: FSMContext):
    pass  # TODO сделать ответ


@router.message(StateFilter(States.AreYou_ULOrIP), F.text == "Да")
async def are_you_ul_or_ip_yes(msg: Message, state: FSMContext):
    await state.set_state(States.IsItEconomicalCase)
    return await msg.answer("Связан ли спор с предпринимательской или иной экономической деятельностью")


@router.message(StateFilter(States.IsItEconomicalCase), F.text == "Да")
async def is_it_economical_case_yes(msg: Message, state: FSMContext):
    await state.set_state(States.IsYourDefendant_ULOrIP)
    return await msg.answer(
        "Ответчик является юридическим лицом, или спор связан с его статусом индивидуального предпринимателя?"
    )


@router.message(StateFilter(States.IsYourDefendant_ULOrIP), F.text == "Нет")
async def is_your_defendant_ul_or_ip_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsYourDefendentCountry)
    return await msg.answer("Спор связан с оспариванием действий государственных органов?")


@router.message(StateFilter(States.IsYourDefendentCountry), F.text == "Да")  # TODO Арбитражный суд
async def is_your_defendant_country_yes(msg: Message, state: FSMContext):
    await state.set_state(States.IsYourDefendentArbitrationCourt)
    return await msg.answer("Вы спорите с арбитражным судом? (Просим одуматься)")


@router.message(StateFilter(States.IsYourDefendentArbitrationCourt), F.text == "Да")
async def is_your_defendant_arbitration_court_yes(msg: Message, state: FSMContext):
    await state.set_state(States.IsItMoscowArbitrationCourt)
    return await msg.answer("Вы спорите с арбитражным судом? (Просим одуматься)")


@router.message(StateFilter(States.IsItMoscowArbitrationCourt), F.text == "Да")
async def is_it_moscow_arbitration_court_yes(msg: Message, state: FSMContext):
    await state.set_state(None)
    return await msg.answer("Арбитражный суд Тверской области")


@router.message(StateFilter(States.IsItMoscowArbitrationCourt), F.text == "Нет")
async def is_it_moscow_arbitration_court_no(msg: Message, state: FSMContext):
    await state.set_state(None)
    return await msg.answer("Арбитражный суд Московской области")


@router.message(StateFilter(States.IsYourDefendentArbitrationCourt), F.text == "Нет")
async def is_your_defendant_arbitration_court_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsIt_FSSP)
    return await msg.answer("Оспариваются действия федеральной службы судебных приставов")


@router.message(StateFilter(States.IsIt_FSSP), F.text == "Да")  # TODO Сделать обработку адреса
async def is_it_fssp_yes(msg: Message, state: FSMContext):
    await state.set_state(None)
    return await msg.answer("Укажите адрес судебного пристава-исполнителя")


@router.message(StateFilter(States.IsIt_FSSP), F.text == "Нет")
async def is_it_fssp_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsItRealtyCase)
    return await msg.answer("Спор связан с недвижимым имуществом?")


@router.message(StateFilter(States.IsItRealtyCase), F.text == "Да")  # TODO Сделать обработку адреса
async def is_it_realty_case_yes(msg: Message, state: FSMContext):
    await state.set_state(None)
    return await msg.answer("Укажите адрес имущества")


@router.message(StateFilter(States.IsItRealtyCase), F.text == "Нет")
async def is_it_realty_case_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsItSpace)
    return await msg.answer("Спор с правами на морские и воздушные суда, суда внутреннего плавания, космические объекты?")


@router.message(StateFilter(States.IsItSpace), F.text == "Да")  # TODO Сделать обработку адреса
async def is_it_space_yes(msg: Message, state: FSMContext):
    await state.set_state(None)
    return await msg.answer("Укажите адрес регистрации имущества")


@router.message(StateFilter(States.IsItSpace), F.text == "Нет")  # TODO Сделать обработку адреса
async def is_it_space_no(msg: Message, state: FSMContext):
    await state.set_state(None)
    return await msg.answer("Укажите адрес ответчика")
