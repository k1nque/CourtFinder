from enum import Enum


class CourtTypeL0(str, Enum):
    General = "general"
    Arbitration = "arbitration"
    IntellectualProperties = "intellectual_properties"
    Military = "military"
    