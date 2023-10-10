from enum import Enum


class Benchmark(str, Enum):
    """
    List of popular interest rate benchmarks.
    """

    LIBOR_USD_3M = "LIBOR_USD_3M"
    LIBOR_USD_6M = "LIBOR_USD_6M"
    ESTER = "ESTER"
