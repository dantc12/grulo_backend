from dataclasses import dataclass


@dataclass
class Place:
    name: str
    type: str

    def __hash__(self):
        return f"{self.name}_{self.type}".__hash__()
