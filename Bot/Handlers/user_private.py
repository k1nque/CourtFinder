from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


user_private_router = Router()


class Test(StatesGroup):
    IsItCriminalCase = State()
    IsItMilitaryServiceCase = State()
    WasCaseBefore = State()
    IsItIntellectualCase = State()
    IsItLegalProtectionCase = State()
    FOIP_ActsChallengeCase = State()
    LongIntellectual = State()
    IsItCopyRightCase = State()
    IsItEntrepreneurialActivityCase = State()
    IsItBankruptcyCase = State()
    IsRelatedWithLegalEntityStatus = State()
    ChallengingWithLegalEntityCase = State()
    ChallengingGovernmentActionsCase = State()
    IsRussianCourtCase = State()
    IsItForeignEntrepreneurialActivityCase = State()
    AddressOfDebtorNotEntrepreneurial = State()
    LocationOfPropertyNotEntrepreneurial = State()
    AddressOfDebtorEntrepreneurial = State()
    LocationOfPropertyEntrepreneurial = State()
    JudgmentInforced = State()
    Past3Months = State()
    ValidReasons2RestoreDeadlines = State()
    CourtMadeDecision = State()


@user_private_router.message(CommandStart())
async def start(msg: types.Message):
    await msg.answer(
        "Доброго времени суток!\n Если Вы хотите узнать в какой суд "
        "вам следует обратиться, выполните команду /start_test"
    )


@user_private_router.message(StateFilter(None), Command("start_test"))
async def start_test(msg: types.Message, state: FSMContext):
    await msg.answer("Есть ли нарушение в УК?")
    await state.set_state(Test.IsItCriminalCase)


@user_private_router.message(StateFilter(Test.IsItCriminalCase), F.text == "Нет")
async def is_it_military_service_case(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с военной службой?")
    await state.set_state(Test.IsItMilitaryServiceCase)


@user_private_router.message(StateFilter(Test.IsItMilitaryServiceCase), F.text == "Нет")
async def was_case_before(msg: types.Message, state: FSMContext):
    await msg.answer("Рассматривалось ли дело ранее?")
    await state.set_state(Test.WasCaseBefore)


@user_private_router.message(StateFilter(Test.WasCaseBefore), F.text == "Нет")
async def is_it_intellectual_case(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Спор связан с результатами интеллектуальной деятельности и приравненным к ним средствам индивидуализации?"
    )
    await state.set_state(Test.IsItIntellectualCase)
    
    
@user_private_router.message(StateFilter(Test.WasCaseBefore), F.text == "Да")
async def is_it_russian_court(msg: types.Message, state: FSMContext):
    await msg.answer("Суд Российский?")
    await state.set_state(Test.IsRussianCourtCase)
    
    
     
@user_private_router.message(StateFilter(Test.WasCaseBefore), F.text == "Нет")
async def is_it_foreign_entrepreneurial_acrivity_case(msg: types.Message, state: FSMContext):
    await msg.answer("Связан ли спор с предпринимательской или другой экономической деятельностью")
    await state.set_state(Test.AddressOfDebtorNotEntrepreneurial)
    

@user_private_router.message(StateFilter(Test.AddressOfDebtorNotEntrepreneurial), F.text == "Не знаю") # TODO
async def address_of_debtor_not_entrepreneurial(msg: types.Message, state: FSMContext):
    await msg.answer("Введите место нахождения имущества")
    await state.set_state(Test.LocationOfPropertyNotEntrepreneurial) 
   
   
@user_private_router.message(StateFilter(Test.LocationOfPropertyNotEntrepreneurial), F.text)
async def location_of_property_not_entrepreneurial(msg: types.Message, state: FSMContext):
    await general_jurisdiction_court_of_subject(msg, state)
    
    
@user_private_router.message(StateFilter(Test.IsItForeignEntrepreneurialActivityCase), F.text == "Да")
async def address_of_debor_entrepreneurial(msg: types.Message, state: FSMContext):
    await msg.answer("Введите место жительства должника")
    await state.set_state(Test.AddressOfDebtorEntrepreneurial)
    
    
@user_private_router.message(StateFilter(Test.AddressOfDebtorEntrepreneurial), F.text == "Не знаю")
async def location_of_property_entrepreneurial(msg: types.Message, state: FSMContext):
    await msg.answer("Введите место нахождения имущества")
    await state.set_state(Test.LocationOfPropertyEntrepreneurial)
    
    
@user_private_router.message(StateFilter(Test.LocationOfPropertyEntrepreneurial), F.text)
async def location_of_property_entrepreneurial(msg: types.Message, state: FSMContext):
    await arbitral_court_of_subject(msg, state)

    
@user_private_router.message(StateFilter(Test.IsItIntellectualCase), F.text == "Нет")
async def it_it_intellectual_case_no(msg: types.Message, state: FSMContext):
    await is_it_entrepreneurial_activity_case(msg, state)


@user_private_router.message(StateFilter(Test.IsItIntellectualCase), F.text == "Да")
async def is_it_legal_protection_case(msg: types.Message, state: FSMContext):
    await msg.answer("спор о предоставлении/прекращении правовой охраны?")
    await state.set_state(Test.IsItLegalProtectionCase)


@user_private_router.message(StateFilter(Test.IsItLegalProtectionCase), F.text == "Нет")
async def FOIP_acts_challenge_case(msg: types.Message, state: FSMContext):
    await msg.answer("Оспариваются акты ФОИП?")
    await state.set_state(Test.FOIP_ActsChallengeCase)
    

@user_private_router.message(StateFilter())
async def FOIP_no(msg: types.Message, state: FSMContext):
    await is_it_entrepreneurial_activity_case(msg, state)
    

@user_private_router.message(StateFilter(Test.FOIP_ActsChallengeCase), F.text == "Да")
async def long_intellectual_case(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Акт связан с патентными правами; правами на селекционные достижения; "
        "правами на топологии интегральных микросхем средства индивидуализации ЮЛ, товаров, работ, услуг, предприятий "
        "Правами на секреты производства правами на использование результатов ИД в составе единой технологии"
    )
    await state.set_state(Test.LongIntellectual)


@user_private_router.message(StateFilter(Test.FOIP_ActsChallengeCase), F.text == "Нет")
async def long_intellectual_no(msg: types.Message, state: FSMContext):
    pass # TODO

@user_private_router.message(StateFilter(Test.LongIntellectual), F.text == "Да")  # TODO
async def long_intellectual_yes(msg: types.Message, state: FSMContext):
    await intellectual_property_court(msg, state)
    
    
@user_private_router.message(StateFilter(Test.LongIntellectual), F.text == "Нет")
async def long_intellectual_no(msg: types.Message, state: FSMContext):
    await is_it_entrepreneurial_activity_case(msg, state)


@user_private_router.message(StateFilter(Test.IsItLegalProtectionCase), F.text == "Да")
async def is_it_copyright_case(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Спор связан с объектами авторских и смежных прав, топологиями интегральных микросхем"
    )
    await state.set_state(Test.IsItCopyRightCase)


@user_private_router.message(StateFilter(Test.IsItCopyRightCase), F.text == "Нет")
async def is_it_copyright_no(msg: types.Message, state: FSMContext):  # TODO
    await intellectual_property_court(msg, state)
    
    
@user_private_router.message(StateFilter(Test.IsItEntrepreneurialActivityCase, F.text == "Нет"))
async def is_it_entrepreneurial_no(msg: types.Message, state: FSMContext):
    await general_jurisdiction_court(msg, state)    
    
    
@user_private_router.message(StateFilter(Test.IsItEntrepreneurialActivityCase), F.text == "Да")
async def is_it_bankruptcy_case(msg: types.Message, state: FSMContext):
    await msg.answer("Связан ли спор с банкротством?")
    await state.set_state(Test.IsItBankruptcyCase)
    
    
@user_private_router.message(StateFilter(Test.IsItBankruptcyCase), F.text == "Нет")
async def is_related_with_legal_entity_status(msg: types.Message, state: FSMContext):
    await msg.answer("Правонарушение связано с вашим статусом Юридического лица / ИП")
    await state.set_state(Test.IsRelatedWithLegalEntityStatus)
    
    
@user_private_router.message(StateFilter(Test.IsRelatedWithLegalEntityStatus), F.text == "Нет")
async def is_related_with_legal_entity_status_no(msg: types.Message, state: FSMContext):
    await general_jurisdiction_court(msg, state)  
    
    
@user_private_router.message(StateFilter(Test.IsRelatedWithLegalEntityStatus), F.text == "Да")
async def challenging_with_legal_entity_case(msg: types.Message, state: FSMContext):
    await msg.answer("Вы судитесь с Юридическим лицом / ИП?")
    await state.set_state(Test.ChallengingWithLegalEntityCase)
    
    
@user_private_router.message(StateFilter(Test.ChallengingWithLegalEntityCase), F.text == "Нет")
async def challenging_government_actions_case(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с оспариванием действий гос органов?")
    await state.set_state(Test.ChallengingGovernmentActionsCase)
    
    
@user_private_router.message(StateFilter(Test.ChallengingGovernmentActionsCase), F.text == "Нет")
async def challenging_government_actions_case_no(msg: types.Message, state: FSMContext):
    await general_jurisdiction_court(msg, state)
    
    
@user_private_router.message(StateFilter(Test.ChallengingGovernmentActionsCase), F.text == "Да")
async def challenging_government_actions_case_yes(msg: types.Message, state: FSMContext):
    await arbitral_court(msg, state)
    
    
# "__________________________________________________________________________________________________________________________________________________________"


async def is_it_entrepreneurial_activity_case(msg: types.Message, state: FSMContext):
    await msg.answer("Связан ли спор с предприниматьельской или другой экономической деятельностью")
    await state.set_state(Test.IsItEntrepreneurialActivityCase)


async def intellectual_property_court(msg: types.Message, state: FSMContext):  # TODO
    await msg.answer("Суд по Интеллектуальным правам")
    
    
async def general_jurisdiction_court(msg: types.Message, state: FSMContext): # TODO
    await msg.answer("Суды общей Юрисдикции")


async def arbitral_court(msg: types.Message, state: FSMContext): # TODO
    await msg.answer("Арбитражные суды")
    
    
async def arbitral_court_of_subject(msg: types.Message, state: FSMContext):
    await msg.answer("Арбитражный суд субъекта")
    
    
async def general_jurisdiction_court_of_subject(msg: types.Message, state: FSMContext):
    await msg.answer("СОЮ Субъекта")