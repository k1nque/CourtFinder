from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    RegulationChallenging = State()
    FOIP = State()
    Copyright = State()
    TrademarkTermination = State()
    NotSatisfiedWithEntryInRegistry = State()
    Rospatent = State()
