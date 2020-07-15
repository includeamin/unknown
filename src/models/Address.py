from pydantic import BaseModel


class AddressString(BaseModel):
    address: str
