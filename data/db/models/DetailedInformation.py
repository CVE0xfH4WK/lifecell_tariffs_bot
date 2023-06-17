import datetime

from beanie import Document


class DetailedInformation(Document):
    tariff_name: str
    details_page_link: str

    class Settings:
        use_cache = True
        cache_expiration_time = datetime.timedelta(seconds=10)
        cache_capacity = 25
