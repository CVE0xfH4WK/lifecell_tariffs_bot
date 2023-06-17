from bot.data_provider import data_provider


async def closest_value():
    data = await data_provider.get_tariffs_overview()

    for item in data:
        print(item.min_price)
                


