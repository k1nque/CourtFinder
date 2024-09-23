from enum import Enum


class ArbitrationCourtTypes(str, Enum):
    Subject = "subject",
    District = "district",
    Appeal = "appeal",
    Intellectual = "intellectual"    
    