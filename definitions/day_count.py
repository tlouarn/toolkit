from enum import Enum


class DayCount(str, Enum):
    ACT_360 = "ACT/360"
    ACT_365 = "ACT/365"
