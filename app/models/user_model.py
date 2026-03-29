from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password: str

    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        return cls(id=row[0], username=row[1], password=row[2])

    def to_public_dict(self):
        return {"id": self.id, "username": self.username}
