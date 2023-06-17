import asyncio
from pathlib import Path

import aiofiles
from pydantic import BaseModel

from data.db import init_connection
from data.db.models.DetailedInformation import DetailedInformation
from data.db.models.GeneralTariffInfo import GeneralTariffInfo
from data.db.models.Tariffs import Tariffs
from data.parser.pages.parse_detailed_info import parse_detailed_info
from data.parser.pages.parse_tariff_overview import parse_tariff_overview
from data.parser.utils.setup_driver import setup_driver
from shared.config import config
from shared.logger import get_logger, setup_loggers

EXPORT_DIR = config.parser.relative_export_directory
logger = get_logger(__name__)


# TODO: Make a brief cli tool for clearing all the data and parsing with saving in different variants
# TODO: Make a driver pool when the detailed info parsing is implemented
async def parse_everyting() -> Tariffs:
    logger.info('Pasing all the data from lifecell')
    driver = setup_driver()

    tariffs_overview = await parse_tariff_overview(driver)
    info_to_insert: list[DetailedInformation] = []

    for tariff in tariffs_overview:
        single_page_data = await parse_detailed_info(driver, tariff.details_page_link)
        info_to_insert.append(single_page_data)

    await DetailedInformation.insert_many(info_to_insert)

    tariffs = Tariffs(
        tarrifs_overview=tariffs_overview,
        detailed_information=info_to_insert
    )

    logger.debug(f'The resulting parsed data {tariffs = }')

    driver.close()
    logger.info('Closed the WebDriver')

    return tariffs


async def export_to_json(export_file: Path, data: BaseModel) -> None:
    async with aiofiles.open(
        export_file,
        'w+'
    ) as handle:
        await handle.write(data.json())

    logger.info(f'Exported the parsing results to {export_file = }')


# TODO: Abstract the logic into the Tariffs class
async def gather_and_save(export_dir: Path) -> Tariffs:
    present_general_data = await GeneralTariffInfo.find_all().to_list()
    present_detailed_data = await DetailedInformation.find_all().to_list()

    present_data = Tariffs(
        tarrifs_overview=present_general_data,
        detailed_information=present_detailed_data
    )

    logger.debug(f'Already present db tariff data: {present_data}')

    if len(present_general_data) >= 1 and len(present_detailed_data):
        logger.info('Skipping parsing as the parsed data is already present in the db')

        return present_data

    tariffs = await parse_everyting()

    # TODO: A config option to either export into json or save to the db
    export_file = export_dir.joinpath('tariffs.json')
    await export_to_json(export_file, tariffs)

    return tariffs


async def main() -> None:
    setup_loggers()
    await init_connection()

    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir()

        logger.debug(
            f'The directory especified as the export dir in the config did not exists, created {EXPORT_DIR = }'
        )

    await gather_and_save(EXPORT_DIR)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
