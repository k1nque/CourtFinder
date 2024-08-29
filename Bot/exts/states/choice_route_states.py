from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
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
