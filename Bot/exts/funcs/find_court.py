from aiogram.fsm.context import FSMContext
from ..enums import CourtType, GeneralCourtType
from .api_call import get_courts


async def find_court(fias: str, state: FSMContext) -> dict[str, str]:
    data = await state.get_data()
    court_l0 = data.get("court_l0")
    court_l1 = data.get("court_l1")
    
    courts = await get_courts(fias)
    
    match court_l0:
        case CourtType.General:
            match court_l1:
                case GeneralCourtType.Magistrate:
                    return courts[0]
                case GeneralCourtType.District:
                    return courts[1]
                case GeneralCourtType.Subject:
                    return courts[2]
                case _:
                    raise AttributeError("Court type L1 exception")
        case _:
            raise AttributeError("Court type L0 exception")
        