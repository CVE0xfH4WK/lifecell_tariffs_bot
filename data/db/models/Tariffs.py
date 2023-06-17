from pydantic import BaseModel

from data.db.models.DetailedInformation import DetailedInformation
from data.db.models.GeneralTariffInfo import GeneralTariffInfo


class Tariffs(BaseModel):
    tarrifs_overview: list[GeneralTariffInfo]
    detailed_information: list[DetailedInformation]
