from enum import Enum
from pathlib import Path

class Directories(Enum):
    DATA = Path("../data")

for directory in Directories:
    directory.value.mkdir(exist_ok=True)