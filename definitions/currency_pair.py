from __future__ import annotations

from dataclasses import dataclass

from definitions.currency import Currency
from shared.exceptions import ToolkitException


class InvalidCurrencyPair(ToolkitException):
    pass


@dataclass
class CurrencyPair:
    base: Currency
    quote: Currency

    def __str__(self) -> str:
        return f"{self.base.value}{self.quote.value}"

    @classmethod
    def parse(cls, string: str) -> CurrencyPair:
        """
        Instantiate a CurrencyPair from a string.
        Expected string format is "EURUSD".
        """
        if len(string) != 6:
            raise InvalidCurrencyPair(string)

        base = Currency(string[0:3])
        quote = Currency(string[3:6])

        if base not in list(Currency) or quote not in list(Currency):
            raise InvalidCurrencyPair(string)

        return cls(base=base, quote=quote)
