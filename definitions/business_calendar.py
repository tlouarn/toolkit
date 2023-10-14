from holidays import country_holidays

from definitions.business_day import BusinessDayConvention, adjust_date
from definitions.date import Date
from definitions.period import Days, Period


class BusinessCalendar:
    def __init__(self, identifier: str, convention: BusinessDayConvention) -> None:
        self.identifier = identifier

        # TODO check for errors
        self.holidays = country_holidays(identifier)
        self.convention = convention

    def add_business_days(self, date: Date, days: int) -> Date:
        """
        Add a given number of good business days to a date.
        :param date: start date
        :param days: number of business days
        :return: good business date
        """
        remaining_days = days
        while remaining_days != 0:
            date = adjust_date(date + Days(1), self.holidays, self.convention)
            remaining_days -= 1
        return date

    def add_period(self, date: Date, period: Period) -> Date:
        """
        Add a given period to a date and adjust the resulting date given holidays
        and business day convention.

        :param date: initial date
        :param period: period
        :return: adjusted end date
        """
        return adjust_date(date + period, self.holidays, self.convention)
