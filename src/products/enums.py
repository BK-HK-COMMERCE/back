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
