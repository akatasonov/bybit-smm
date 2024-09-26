from typing import Dict, Union
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union

@dataclass
class Balance:
    symbol: str
    free: float
    locked: float

class Balances:
    """
    A class to manage a collection of Balance objects.

    Attributes
    ----------
    _balances : Dict[str, Balance]
        A dictionary to store balances with symbol as the key.
    """


    def __init__(self) -> None:
        self._balances: Dict[str, Balance] = {}

    def reset(self) -> None:
        """
        Resets the collection, removing all orders.
        """
        self._balances.clear()

    def recordable(self) -> List[Dict]:
        """
        Unwraps the internal structures into widely-used Python structures
        for easy recordability (databases, logging, debugging etc).

        Returns
        -------
        List[Dict]
            A list of Order objects.
        """
        return [order.to_dict() for order in self._orders_.values()]

    def update(self, symbol: str, free: float, locked: float) -> None:
        """
        Updates a single balance in the collection.

        Parameters
        ----------
        symbol : str
            The symbol of the balance to update.
        free : float
            The free balance.
        locked : float
            The locked balance.
        """
        self._balances.update({symbol: Balance(symbol, free, locked)})

    def __getitem__(self, idx: str) -> Balance:
        return self._balances.get(idx, Balance())

    def __len__(self) -> int:
        return len(self._balances)

    def __repr__(self) -> str:
        return f"Balances({self._balances})"

    def __iter__(self):
        return iter(self._balances.values())
