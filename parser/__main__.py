import asyncio
from parser.pages.parse_tariff_overview import parse_tariff_overview
from pathlib import Path

import aiofiles

EXPORT_DIR = Path('./export')

async def main() -> None:
    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir()

    tariff_overview = await parse_tariff_overview()

    async with aiofiles.open(
        EXPORT_DIR.joinpath('tariff_overview.json'),
        'w+'
    ) as handle:
        await handle.write(tariff_overview.json())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
