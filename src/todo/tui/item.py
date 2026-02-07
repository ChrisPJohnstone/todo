from dataclasses import dataclass, field


@dataclass(frozen=True)
class Item:
    id: int
    created_at: str = field(repr=False)
    message: str
    due: str = field(repr=False)
    completed: str = field(repr=False)
    completed_at: str = field(repr=False)
