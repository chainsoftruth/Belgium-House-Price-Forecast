from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class PropertyType(str, Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"
    OTHERS = "OTHERS"

class PropertySubtype(str, Enum):
    STUDIO = "STUDIO"
    CHALET = "CHALET"
    GROUND_FLOOR = "GROUND-FLOOR"
    APARTMENT = "APARTMENT"
    BUNGALOW = "BUNGALOW"
    TRIPLEX = "TRIPLEX"
    DUPLEX = "DUPLEX"
    RESIDENCE = "RESIDENCE"
    MIXED_BUILDING = "MIXED-BUILDING"
    LOFT = "LOFT"
    COTTAGE = "COTTAGE"
    PENTHOUSE = "PENTHOUSE"
    MASTER_HOUSE = "MASTER-HOUSE"
    VILLA = "VILLA"
    MANSION = "MANSION"

class PropertyState(str, Enum):
    NEW = "NEW"
    GOOD = "GOOD"
    TO_RENOVATE = "TO RENOVATE"
    JUST_RENOVATED = "JUST RENOVATED"
    TO_REBUILD = "TO REBUILD"
    EXCELLENT = "EXCELLENT"

class PropertyData(BaseModel):
    area: int
    property_type: PropertyType = Field(alias="property-type")
    property_subtype: PropertySubtype = Field(alias="property-subtype")
    rooms_number: Optional[int] = Field(default=None, alias="rooms-number")
    zip_code: int = Field(alias="zip-code")
    land_area: Optional[int] = Field(default=None, alias="land-area")
    garden: Optional[bool] = None
    garden_area: Optional[int] = Field(default=None, alias="garden-area")
    equipped_kitchen: Optional[bool] = Field(default=None, alias="equipped-kitchen")
    full_address: Optional[str] = Field(default=None, alias="full-address")
    swimming_pool: Optional[bool] = Field(default=None, alias="swimming-pool")
    furnished: Optional[bool] = None
    open_fire: Optional[bool] = Field(default=None, alias="open-fire")
    terrace: Optional[bool] = None
    terrace_area: Optional[int] = Field(default=None, alias="terrace-area")
    facades_number: Optional[int] = Field(default=None, alias="facades-number")
    building_state: Optional[PropertyState] = Field(default=None, alias="building-state")

    class Config:
        extra = "forbid"

class PropertyRequest(BaseModel):
    data: PropertyData