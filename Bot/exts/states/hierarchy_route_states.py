from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    IsYourDefendentCountry = State()
    IsItFederal = State()
    IsItSubjectOrMunicipal = State()
    IsItDivorce = State()
    IsItChildrenCase = State()
    AreTheyLess18 = State()
    IsItLess50K = State()
    IsItInheritanceOrIP = State()
    ZPP = State()
    ZPP_Less100K = State()
    IsItRightCase = State()
    IsItTopSecret = State()