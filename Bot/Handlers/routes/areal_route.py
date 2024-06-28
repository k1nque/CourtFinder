from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

ArealRouter = Router()


class ArealRouteStates(StatesGroup):
    IsItRealtyCase = State()
    IsItinheritance = State()
    IsItGroupCase = State()
    IsItContract = State()
    IsIttransportation = State()
    IsItContractualjurisdiction = State()
    ThePlaceOfExecutionIsIndicated = State()
    IsItHealthHarm = State()
    IsItDadCase = State()
    IsItCollisionOfShips = State()
    IsItJobCase = State()
    IsItZPPCase = State()
    IsItPersonalDataCase = State()
    IsItBranchCase = State()
    IsYourDefendentinRF = State()


# TODO переход из hierarchy_route


@ArealRouter.message(StateFilter(ArealRouteStates.IsItRealtyCase), F.text == "Да")
async def is_it_realty_case_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес земельного участка")
    await state.set_state(None)


@ArealRouter.message(StateFilter(ArealRouteStates.IsItRealtyCase), F.text == "Нет")
async def is_it_realty_case_no(msg: types.Message, state: FSMContext):
    await msg.answer("Вы кредитор умершего, а наследники еще не приняли наследство?")
    await state.set_state(ArealRouteStates.IsItinheritance)


@ArealRouter.message(StateFilter(ArealRouteStates.IsItinheritance), F.text == "Да")
async def is_it_inheritance_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес открытия наследства")
    await state.set_state(None)


@ArealRouter.message(StateFilter(ArealRouteStates.IsItinheritance), F.text == "Нет")
async def is_it_inheritance_no(msg: types.Message, state: FSMContext):
    await msg.answer("Иск о защите группы лиц?")
    await state.set_state(ArealRouteStates.IsItGroupCase)



@ArealRouter.message(StateFilter(ArealRouteStates.IsItGroupCase), F.text == "Да")
async def is_it_group_case_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес ответчика")
    await state.set_state(None)


@ArealRouter.message(StateFilter(ArealRouteStates.IsItGroupCase), F.text == "Нет")
async def is_it_group_case_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор следует из договора?")
    await state.set_state(ArealRouteStates.IsItContract)


@ArealRouter.message(StateFilter(ArealRouteStates.IsItContract), F.text == "Да")
async def is_it_contract_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Это договор перевозки?")
    await state.set_state(ArealRouteStates.IsIttransportation)


@ArealRouter.message(StateFilter(ArealRouteStates.IsIttransportation), F.text == "Да")
async def is_it_transportation_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес перевозчика")
    await state.set_state(None)


@ArealRouter.message(StateFilter(ArealRouteStates.IsIttransportation), F.text == "Нет")
async def is_it_transportation_no(msg: types.Message, state: FSMContext):
    await msg.answer("Подсудность определена договором?")
    await state.set_state(ArealRouteStates.IsItContractualjurisdiction)


@ArealRouter.message(StateFilter(ArealRouteStates.IsItContractualjurisdiction), F.text == "Да")
async def is_it_contractual_jurisdiction_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Рекомендуем обратиться в суд, указанный в договоре")
    await state.set_state(None)


@ArealRouter.message(StateFilter(ArealRouteStates.IsItContractualjurisdiction), F.text == "Нет")
async def is_it_contractual_jurisdiction_no(msg: types.Message, state: FSMContext):
    await msg.answer("В договоре определено место исполнения?")
    await state.set_state(ArealRouteStates.ThePlaceOfExecutionIsIndicated)


@ArealRouter.message(StateFilter(ArealRouteStates.ThePlaceOfExecutionIsIndicated), F.text == "Да")
async def the_place_of_execution_is_indicated_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите место исполнения или адрес ответчика")
    await state.set_state(None)


@ArealRouter.message(
    StateFilter(ArealRouteStates.ThePlaceOfExecutionIsIndicated),
    F.text == "Нет",
)
async def the_place_of_execution_is_indicated_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с защитой трудовых прав?")
    await state.set_state(ArealRouteStates.IsItJobCase)


@ArealRouter.message(StateFilter(ArealRouteStates.IsItContract), F.text == "Нет")
async def is_it_contract_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан со столкновением судов?")
    await state.set_state(ArealRouteStates.IsItCollisionOfShips)


@ArealRouter.message(StateFilter(ArealRouteStates.IsItCollisionOfShips), F.text == "Да")
async def is_it_collision_of_ship_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите")
    await state.set_state(ArealRouteStates.IsItCollisionOfShips)
