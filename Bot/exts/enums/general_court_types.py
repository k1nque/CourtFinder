from enum import Enum


class GeneralCourtType(str, Enum):
    District = "district"
    Subject = "subject"
    Magistrate = "magistrate"
    Supreme = "supreme"
