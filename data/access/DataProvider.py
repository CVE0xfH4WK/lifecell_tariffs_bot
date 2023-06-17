from datetime import datetime

from beanie import PydanticObjectId

from data.db.models.GeneralTariffInfo import GeneralTariffInfo
from data.db.models.Tariffs import Tariffs
from shared.logger import get_logger

logger = get_logger(__name__)
Cache = tuple[datetime, Tariffs]

CACHE_EXPIRATION_TIME_SECONDS = 180


class DataProvider:
    def __init__(self) -> None:
        ...

    async def get_tariffs_overview(self) -> list[GeneralTariffInfo] | None:
        data = await GeneralTariffInfo.find_all().sort('+price').to_list()

        return data

    async def get_single_tariff_overview(
        self,
        tarif_id: PydanticObjectId
    ) -> GeneralTariffInfo | None:
        return await GeneralTariffInfo.get(tarif_id)
        
