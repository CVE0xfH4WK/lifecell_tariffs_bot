from parser.schema.DetailedInformation import DetailedInformation
from parser.schema.GeneralOverview import GeneralOverview

from pydantic import BaseModel


class Tariffs(BaseModel):
    general_overview: GeneralOverview
    detailed_information: DetailedInformation
