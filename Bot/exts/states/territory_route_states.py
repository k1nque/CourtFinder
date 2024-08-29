from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    LandPlots = State()
    CreditorsClaim = State()
    DefenseGroup = State()
    ContractDispute = State()
    DamageCompensation = State()
    Alimony = State()
    ShipsColision = State()
    Transportation = State()
    ContractDeterminedJurisdiction = State()
    AddressSpecified = State()
    LaborRightsProtection = State()
    ConsumerProtection = State()
    PersonalData = State()
    BranchActivities = State()
    RF_Residence = State()