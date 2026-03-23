from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class PropertyType(str, Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"

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
    
class Property(BaseModel):
    area: int
    property_type : PropertyType = Field(alias = "property-type")
    property_subtype : PropertySubtype = Field(alias = "property-subtype")
    rooms_number : Optional[int] = Field(alias = "rooms-number")
    zip_code : int = Field(alias = "zip-code")
    land_area : Optional[int] = Field(default = 0, alias = "land-area")
    garden : bool
    garden_area : Optional[int] = Field(alias = "garden-area")
    equipped_kitchen : Optional[bool] = Field(alias = "equipped-kitchen")
    full_address : Optional[str] = Field(alias = "full-address")
    swimming_pool : bool = Field(alias = "swimming-pool")
    furnished : bool
    open_fire : Optional[bool] = Field(alias = "open-fire")
    terrace : bool
    terrace_area : Optional[int] = Field(alias = "terrace-area")
    facades_number : int = Field(alias = "facades-number")
    building_state : PropertyState = Field(alias = "building-state")
    
    class Config:
        extra = "forbid"

class PropertyRequest(BaseModel):
    data: Property