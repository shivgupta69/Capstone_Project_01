from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    id: int
    user_id: int
    task_name: str
    category: str
    duration: int
    due_date: Optional[str] = None
    status: str = "todo"
    estimated_hours: Optional[float] = None
    scheduled_date: Optional[str] = None

    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        return cls(
            id=row[0],
            user_id=row[1],
            task_name=row[2],
            category=row[3],
            duration=row[4],
            due_date=row[5] if len(row) > 5 else None,
            status=row[6] if len(row) > 6 and row[6] else "todo",
            estimated_hours=row[7] if len(row) > 7 else None,
            scheduled_date=row[8] if len(row) > 8 else None,
        )
