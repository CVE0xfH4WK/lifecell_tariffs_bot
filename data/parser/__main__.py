import asyncio
from pathlib import Path

import aiofiles
from pydantic import BaseModel

from data.db import init_connection
from data.db.models.DetailedInformation import DetailedInformation
from data.db.models.Tariffs import Tariffs
from data.parser.pages.parse_detailed_info import parse_detailed_info
from data.parser.pages.parse_tariff_overview import parse_tariff_overview
from data.parser.utils.setup_driver import setup_driver
from shared.config import config
from shared.logger import get_logger, setup_loggers

EXPORT_DIR = config.parser.relative_export_directory
logger = get_logger(__name__)


# TODO: Make a brief cli tool for clearning all the data and parsing with saving in different variants
# TODO: Make a driver pool when the detailed info parsing is implemented
async def parse_everyting() -> Tariffs:
    logger.info('Pasing all the data from lifecell')
    driver = setup_driver()

    tariff_overview = await parse_tariff_overview(driver)
    all_detailed_info: list[DetailedInformation] = []
    for tariff in tariff_overview.tariffs:
        single_page_data = await parse_detailed_info(driver, tariff.details_page_link)
        all_detailed_info.append(single_page_data)

    tariffs = Tariffs(
        general_overview=tariff_overview,
        detailed_information=all_detailed_info
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


async def gather_and_save(export_dir: Path) -> Tariffs:
    present_data = await Tariffs.find_all().to_list()
    logger.debug(f'Already present db tariff data: {present_data = }')

    if len(present_data) >= 1:
        logger.info('Skipping parsing as the parsed data is already present in the db')
        tariffs = present_data[-1]
    else:
        tariffs = await parse_everyting()

        logger.info('Inserting the parsed data into the db')
        await Tariffs.insert(tariffs)

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
