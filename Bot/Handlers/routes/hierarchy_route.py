from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

HierarchyRouter = Router()


class HierarchyRouteStates(StatesGroup):
    IsYourDefendentCountry = State()
    IsItFederal = State()
    IsItSabjectOrmunicipal = State()
    IsItdivorce = State()
    IsItChildrenCase = State()
    AreTheyLess18 = State()
    IsItLess50K = State()
    IsItinheritanceOrIP = State()
    ZPP = State()
    ZPP_Less100K = State()
    IsItRightCase = State()
    IsItTopSecret = State()


    #TODO начало мышь


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsYourDefendentCountry), Text="Да")
async def is_your_defendent_country_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Оспаривается решение федерального органа")
    await state.set_state(HierarchyRouteStates.IsItFederal)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsYourDefendentCountry), Text="Что это?")
async def is_your_defendent_country_what_is_it(msg: types.Message, state: FSMContext):
    await msg.answer #TODO


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItFederal), Text="Да")
async def is_your_defendent_country_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Верховный Суд")
    await state.set_state(None)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItFederal), Text="Нет")
async def is_your_defendent_country_no(msg: types.Message, state: FSMContext):
    await msg.answer("Оспариваются решения органов государственной власти субъектов и представительств муниципальных образований?")
    await state.set_state(HierarchyRouteStates.IsItSabjectOrmunicipal)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsYourDefendentCountry), Text="Нет")
async def is_your_defendent_country_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с расторжением брака?")
    await state.set_state(HierarchyRouteStates.IsItdivorce)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItdivorce), Text="Да")
async def is_it_divorce_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Есть  ли спор о несовершеннолетних детях?")
    await state.set_state(HierarchyRouteStates.IsItChildrenCase)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItdivorce), Text="Нет")
async def is_it_divorce_no(msg: types.Message, state: FSMContext):
    await msg.answer("Вы хотите вернуть сумму до 50 тысяч рублей?")
    await state.set_state(HierarchyRouteStates.IsItLess50K)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItLess50K), Text="Нет")
async def is_it_less_50k_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор о защите прав потребителей?")
    await state.set_state(HierarchyRouteStates.ZPP)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItLess50K), Text="Да")
async def is_it_less50k_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Это наследственный спор?") #TODO посмотреть ответ на вопрос связан ли спор с интеллектуалкой, ответ аналогичен ответу про наследство 
    await state.set_state(HierarchyRouteStates.IsItinheritanceOrIP) #TODO вывод Мировой/районный суд


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.ZPP), Text="Нет")
async def ZPP_no(msg: types.Message, state: FSMContext):
    await msg.answer("Это спор о праве?")
    await state.set_state(HierarchyRouteStates.IsItRightCase)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.ZPP), Text="Да")
async def ZPP_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Спор меньше 100 тысяч рублей?")
    await state.set_state(HierarchyRouteStates.ZPP_Less100K) #TODO выходит в вывод


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItRightCase), Text="Что это?")
async def is_it_right_case_what_is_it (msg: types.Message, state: FSMContext):
    await msg.answer #TODO


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItRightCase), Text="Да?")
async def is_it_right_case_yes (msg: types.Message, state: FSMContext):
    await msg.answer #TODO вывод


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItRightCase), Text="Нет")
async def is_it_right_case_no (msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с государственной тайной?")
    await state.set_state(HierarchyRouteStates.IsItTopSecret)

    #TODO вывод 











    



