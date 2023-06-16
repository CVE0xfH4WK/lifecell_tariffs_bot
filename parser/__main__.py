import asyncio
from parser.pages.parse_detailed_info import parse_detailed_info
from parser.pages.parse_tariff_overview import parse_tariff_overview
from parser.utils.setup_driver import setup_driver

import aiofiles

from config import config

EXPORT_DIR = config.parser.relative_export_directory

# TODO: Make a driver pool when the detailed info parsing is implemented

async def main() -> None:
    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir()

    driver = setup_driver()

    tariff_overview = await parse_tariff_overview(driver)
    for tariff in tariff_overview.tariffs:
        await parse_detailed_info(driver, tariff.details_page_link)

    async with aiofiles.open(
        EXPORT_DIR.joinpath('tariff_overview.json'),
        'w+'
    ) as handle:
        await handle.write(tariff_overview.json())

    driver.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
