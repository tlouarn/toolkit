from enum import Enum

# Useful link
# https://strata.opengamma.io/apidocs/com/opengamma/strata/basics/schedule/StubConvention.html

# TODO implement more STUB, right now we consider all STUBS are short


class StubConvention(str, Enum):
    """
    Stub period conventions:
    - FRONT: the stub is located at the beginning of the schedule
    - BACK: the stub is located at the end of the schedule
    - SHORT: the duration of the stub is less than a regular step
    - LONG: the duration of the stub is longer than a regular step
    """

    FRONT = "Front"
    BACK = "Back"
