from pydantic import BaseModel


class DetailedInformation(BaseModel):
    tariff_name: str
    details_page_link: str
