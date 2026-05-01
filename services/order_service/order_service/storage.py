from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Order:
    id: int
    user_id: int
    item: str
    price: float
    user_name: str
    user_email: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)


class OrderStore:
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
        self._next_id = 1

    def create(
        self,
        *,
        user_id: int,
        item: str,
        price: float,
        user_name: str,
        user_email: str,
    ) -> Order:
        order = Order(
            id=self._next_id,
            user_id=user_id,
            item=item,
            price=price,
            user_name=user_name,
            user_email=user_email,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._orders[order.id] = order
        self._next_id += 1
        return order

    def get(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)

    def list_all(self) -> list[Order]:
        return list(self._orders.values())

    def reset(self) -> None:
        self._orders.clear()
        self._next_id = 1


order_store = OrderStore()


def reset_order_store() -> None:
    order_store.reset()
