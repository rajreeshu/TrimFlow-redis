from dataclasses import dataclass
from typing import BinaryIO

@dataclass
class CustomFile:
    filename: str
    file: BinaryIO
