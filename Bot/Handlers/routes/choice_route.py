from curses.ascii import FS
from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from Handlers.routes.two_questions_route import TwoQuestionsRouteStates

ChoiceRouter = Router()


class ChoiceRouteStates(StatesGroup):
    IsItCrash = State()
    WhoIsCrash = State()
    AreYou_ULOrIP = State()
    IsItEconomicalCase = State()
    IsYourDefendant_ULOrIP = State()
    IsYourDefendentCountry = State()
    IsYourDefendentArbitrationCourt = State()
    IsItMoscowArbitrationCourt = State()
    IsIt_FSSP = State()
    IsItRealtyCase = State()
    IsItSpace = State()


@ChoiceRouter.message(StateFilter(TwoQuestionsRouteStates.IsItIntellectualCase), F.text == "Нет")
async def start_route(msg: types.Message, state: FSMContext):
    await msg.answer("Cпор связан с банкротством?")
    await state.set_state(ChoiceRouteStates.IsItCrash)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsItCrash), F.text == "Да")  # TODO Арбитражный суд
async def is_it_crash_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Чье банкротсвто рассматривается?")
    await state.set_state(ChoiceRouteStates.WhoIsCrash)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.WhoIsCrash), F.text == "Физического лица")
async def Who_is_crash_FL(msg: types.Message, state: FSMContext):
    await msg.answer("укажите адрес места жительства должника")
    # TODO


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.WhoIsCrash), F.text == "Юридического лица")
async def Who_is_crash_UL(msg: types.Message, state: FSMContext):
    await msg.answer("укажите адрес местонахождения ")
    # TODO


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsItCrash), F.text == "Нет")
async def is_it_crash_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с вашим статусом Юридического лица или индивидуального предпринимателя?")
    await state.set_state(ChoiceRouteStates.AreYou_ULOrIP)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.AreYou_ULOrIP), F.text == "Что это?")
async def are_you_ul_or_ip_what_is_it(msg: types.Message, state: FSMContext):
    pass  # TODO сделать ответ


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.AreYou_ULOrIP), F.text == "Да")
async def are_you_ul_or_ip_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Связан ли спор с предпринимательской или иной экономической деятельностью")
    await state.set_state(ChoiceRouteStates.IsItEconomicalCase)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsItEconomicalCase), F.text == "Да")
async def is_it_economical_case_yes(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Ответчик является юридическим лицом, или спор связан с его статусом индивидуального предпринимателя?"
    )
    await state.set_state(ChoiceRouteStates.IsYourDefendant_ULOrIP)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsYourDefendant_ULOrIP), F.text == "Нет")
async def is_your_defendant_ul_or_ip_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с оспариванием действий государственных органов?")
    await state.set_state(ChoiceRouteStates.IsYourDefendentCountry)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsYourDefendentCountry), F.text == "Да")  # TODO Арбитражный суд
async def is_your_defendant_ul_or_ip_no(msg: types.Message, state: FSMContext):
    await msg.answer("Вы спорите с арбитражным судом? (Просим одуматься)")
    await state.set_state(ChoiceRouteStates.IsYourDefendentArbitrationCourt)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsYourDefendentArbitrationCourt), F.text == "Да")
async def is_your_defendant_arbitration_court_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Вы спорите с арбитражным судом? (Просим одуматься)")
    await state.set_state(ChoiceRouteStates.IsItMoscowArbitrationCourt)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsItMoscowArbitrationCourt), F.text == "Да")
async def is_it_moscow_arbitration_court_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Арбитражный суд Тверской области")
    await state.set_state(None)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsItMoscowArbitrationCourt), F.text == "Нет")
async def is_it_moscow_arbitration_court_no(msg: types.Message, state: FSMContext):
    await msg.answer("Арбитражный суд Московской области")
    await state.set_state(None)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsYourDefendentArbitrationCourt), F.text == "Нет")
async def is_your_defendant_arbitration_court_no(msg: types.Message, state: FSMContext):
    await msg.answer("Оспариваются действия федеральной службы судебных приставов")
    await state.set_state(ChoiceRouteStates.IsIt_FSSP)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsIt_FSSP), F.text == "Да")  # TODO Сделать обработку адреса
async def is_it_fssp_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес судебного пристава-исполнителя")
    await state.set_state(None)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsIt_FSSP), F.text == "Нет")
async def is_it_fssp_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с недвижимым имуществом?")
    await state.set_state(ChoiceRouteStates.IsItRealtyCase)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsItRealtyCase), F.text == "Да")  # TODO Сделать обработку адреса
async def is_it_realty_case_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес имущества")
    await state.set_state(None)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsItRealtyCase), F.text == "Нет")
async def is_it_realty_case_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор с правами на морские и воздушные суда, суда внутреннего плавания, космические объекты?")
    await state.set_state(ChoiceRouteStates.IsItSpace)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsItSpace), F.text == "Да")  # TODO Сделать обработку адреса
async def is_it_space_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес регистрации имущества")
    await state.set_state(None)


@ChoiceRouter.message(StateFilter(ChoiceRouteStates.IsItSpace), F.text == "Нет")  # TODO Сделать обработку адреса
async def is_it_space_no(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес ответчика")
    await state.set_state(None)
