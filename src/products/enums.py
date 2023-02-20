from enum import Enum


class DispatchEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class Size(DispatchEnum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


class Category1(DispatchEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    CHILDREN = "CHILDREN"
    UNISEX = "UNISEX"


class Category2(DispatchEnum):
    OUTER = "OUTER"
    TOP = "TOP"
    PANTS = "PANT"
    SHOES = "SHOES"
    UNDERWEAR = "UNDERWEAR"


class Category3(DispatchEnum):
    COAT = "COAT"
    VEST = "VEST"
    CARDIGAN = "CARDIGAN"
    LEATHER = "LEATHER"

    TSHIRT = "TSHIRT"
    SHIRT = "SHIRT"
    HOODIES = "HOODIES"
    SWEATSHIRT = "SWEATSHIRT"
    DRESS = "DRESS"

    SHORT = "SHORT"
    JEANS = "JEANS"
    SKIRT = "SKIRT"

    BOOTS = "BOOTS"
    SNEAKERS = "SNEAKERS"
    SANDALS = "SANDALS"

    PANTIES = "PANTIES"
    BRA = "BRA"


