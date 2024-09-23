from aiogram.fsm.context import FSMContext

from exts.enums import CourtType, GeneralCourtType, ArbitrationCourtTypes
from .api_call import get_courts, get_arbitration_subject_court


async def find_court(fias: str, state: FSMContext) -> dict[str, str]:
    data = await state.get_data()
    court_l0 = data.get("court_l0")
    court_l1 = data.get("court_l1")
    
    match court_l0:
        case CourtType.General:
            courts = await get_courts(fias)
            if len(courts) < 3:
                return None
            match court_l1:
                case GeneralCourtType.Magistrate:
                    return courts[0]
                case GeneralCourtType.District:
                    return courts[1]
                case GeneralCourtType.Subject:
                    return courts[2]
                case _:
                    raise AttributeError("Court type L1 exception")
        case CourtType.Arbitration:
            match court_l1:
                case ArbitrationCourtTypes.Subject:
                    suggs: list[dict[str, str]] | None = (await state.get_data()).get("suggestions")
                    if suggs:
                        for sugg in suggs:
                            if sugg["fias"] == fias:
                                region = sugg["region"]
                                if region in (
                                    "Москва",
                                    "Санкт-Петербург",
                                    "Севастополь",
                                ):
                                    r = region
                                else:
                                    region_type_full = sugg["region_type_full"]
                                    region_with_type = sugg["region_with_type"]
                                    if region_with_type.lower().split().index(region.lower()) == 0:
                                        r = (region + " " + region_type_full)
                                    else:
                                        r = (region_type_full + " " + region)
                                    if region_type_full == "республика":
                                        r = r.title()
                                ans_data = await get_arbitration_subject_court(r)
                                return {
                                    "NAME": ans_data["name"],
                                    "ADDRESS": ans_data["address"],
                                    "LINK": ans_data["link"]
                                }
                case ArbitrationCourtTypes.District:
                    pass
                case ArbitrationCourtTypes.Appeal:
                    pass
                case ArbitrationCourtTypes.Intellectual:
                    pass
                case _:
                    raise AttributeError("Court type L1 exception")
        case _:
            raise AttributeError("Court type L0 exception")
        