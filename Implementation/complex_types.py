from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class alignment:
    kind: str
    __VALID_ALIGNMENTS:ClassVar[list[str]] = ['L', 'C', 'R']

    def __post_init__(self):
        if self.kind not in self.__VALID_ALIGNMENTS:
            raise ValueError(f"Invalid alignment >> {self.kind} <<. Must be from {self.__VALID_ALIGNMENTS}")

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        
        if isinstance(other, str):
            return other == self.kind

        if isinstance(other, alignment):
            return other.kind == self.kind

        return False

    def __str__(self) -> str:
        return self.kind


@dataclass
class layout_row:
    word:str
    translation:str
    document_column:int
    document_row:int
    font_size:int
    alignment:alignment


@dataclass
class row:
    coords:list[list[int]]
    word:str
    translation:str = ""
    lines:int = 1

    def __post_init__(self):
        x_1, y_1 = self.coords[0]
        x_2, y_2 = self.coords[1]
        x_3, y_3 = self.coords[2]
        x_4, y_4 = self.coords[3]

        x_min = int(min(x_1, x_4))
        x_max = int(max(x_2, x_3))
        y_min = int(min(y_1, y_2))
        y_max = int(max(y_3, y_4))

        self.rect:list[int] = [x_min, x_max, y_min, y_max]

    def __str__(self) -> str:
        return f"row({self.word}, {self.translation}, [{self.rect[0]}, {self.rect[1]}, {self.rect[2]}, {self.rect[3]}])"


@dataclass
class raw_row:
    coords:list[list[int]]
    word:str


@dataclass
class buffer_row:
    word:str
    translation:str

