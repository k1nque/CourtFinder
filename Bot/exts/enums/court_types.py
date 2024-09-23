from enum import Enum


class CourtType(str, Enum):
    General = "general"
    Arbitration = "arbitration"
    IntellectualProperties = "intellectual_properties"
    Military = "military"
    