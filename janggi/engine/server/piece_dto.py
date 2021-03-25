import dataclasses

from typing import List


@dataclasses.dataclass
class PieceDTO:
    Position: List[int]
    Color: str
    Category: str
