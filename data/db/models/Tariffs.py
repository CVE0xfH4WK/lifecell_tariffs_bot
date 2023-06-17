from beanie import Document

from data.db.models.DetailedInformation import DetailedInformation
from data.db.models.GeneralOverview import GeneralOverview


class Tariffs(Document):
    general_overview: GeneralOverview
    detailed_information: list[DetailedInformation]
