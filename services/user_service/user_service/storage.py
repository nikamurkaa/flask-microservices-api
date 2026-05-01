from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str

    def to_dict(self) -> dict:
        return asdict(self)


class UserStore:
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._next_id = 1

    def create(self, *, name: str, email: str) -> User:
        user = User(id=self._next_id, name=name, email=email)
        self._users[user.id] = user
        self._next_id += 1
        return user

    def get(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    def list_all(self) -> list[User]:
        return list(self._users.values())

    def reset(self) -> None:
        self._users.clear()
        self._next_id = 1


user_store = UserStore()


def reset_user_store() -> None:
    user_store.reset()
