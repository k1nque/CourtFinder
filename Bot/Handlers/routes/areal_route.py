from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from exts.states import ArealRouteStates as States


router = Router()

# TODO переход из hierarchy_route


@router.message(StateFilter(States.IsItRealtyCase), F.text == "Да")
async def is_it_realty_case_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес земельного участка")
    await state.set_state(None)


@router.message(StateFilter(States.IsItRealtyCase), F.text == "Нет")
async def is_it_realty_case_no(msg: types.Message, state: FSMContext):
    await msg.answer("Вы кредитор умершего, а наследники еще не приняли наследство?")
    await state.set_state(States.IsItinheritance)


@router.message(StateFilter(States.IsItinheritance), F.text == "Да")
async def is_it_inheritance_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес открытия наследства")
    await state.set_state(None)


@router.message(StateFilter(States.IsItinheritance), F.text == "Нет")
async def is_it_inheritance_no(msg: types.Message, state: FSMContext):
    await msg.answer("Иск о защите группы лиц?")
    await state.set_state(States.IsItGroupCase)



@router.message(StateFilter(States.IsItGroupCase), F.text == "Да")
async def is_it_group_case_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес ответчика")
    await state.set_state(None)


@router.message(StateFilter(States.IsItGroupCase), F.text == "Нет")
async def is_it_group_case_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор следует из договора?")
    await state.set_state(States.IsItContract)


@router.message(StateFilter(States.IsItContract), F.text == "Да")
async def is_it_contract_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Это договор перевозки?")
    await state.set_state(States.IsIttransportation)


@router.message(StateFilter(States.IsIttransportation), F.text == "Да")
async def is_it_transportation_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес перевозчика")
    await state.set_state(None)


@router.message(StateFilter(States.IsIttransportation), F.text == "Нет")
async def is_it_transportation_no(msg: types.Message, state: FSMContext):
    await msg.answer("Подсудность определена договором?")
    await state.set_state(States.IsItContractualjurisdiction)


@router.message(StateFilter(States.IsItContractualjurisdiction), F.text == "Да")
async def is_it_contractual_jurisdiction_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Рекомендуем обратиться в суд, указанный в договоре")
    await state.set_state(None)


@router.message(StateFilter(States.IsItContractualjurisdiction), F.text == "Нет")
async def is_it_contractual_jurisdiction_no(msg: types.Message, state: FSMContext):
    await msg.answer("В договоре определено место исполнения?")
    await state.set_state(States.ThePlaceOfExecutionIsIndicated)


@router.message(StateFilter(States.ThePlaceOfExecutionIsIndicated), F.text == "Да")
async def the_place_of_execution_is_indicated_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите место исполнения или адрес ответчика")
    await state.set_state(None)


@router.message(
    StateFilter(States.ThePlaceOfExecutionIsIndicated),
    F.text == "Нет",
)
async def the_place_of_execution_is_indicated_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с защитой трудовых прав?")
    await state.set_state(States.IsItJobCase)


@router.message(StateFilter(States.IsItContract), F.text == "Нет")
async def is_it_contract_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан со столкновением судов?")
    await state.set_state(States.IsItCollisionOfShips)


@router.message(StateFilter(States.IsItCollisionOfShips), F.text == "Да")
async def is_it_collision_of_ship_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите")
    await state.set_state(States.IsItCollisionOfShips)
