## Principles

### 1.1 Pure-python

### `Decimal` over `float`
Decimal type is preferred for values.
Slower but exact. Important to be able to infer input from output and not math.isclose() with floats.
floats are fast but lack precisions
should we use Decimal for all calculations?

### 1.2 Pythonic

Different: a code can be pure python but not "pythonic". Being pythonic means leveraging on the 
language's features.

Javaesque: `date.to_string()`
Pythonic: `str(date)` via dunder functions

Javaesque: `schedule.length()`
Pythonic: `len(schedule)`

operator overload especially with dates and periods

### 1.3 Readability

no complex one-liners

### 1.4 Terminology consistency
Difficulties with the terminology: a same concept can be named differently
by market practitioners. 

Conceptual difficulties: need to group conceptually-linked concepts together
e.g. an InterestRate can't be defined without a DayCount (or a Compounding)

Common conventions: `start` and `end` are dates.
This avoids having to always specify `start_date`, `end_date`.
When synonyms, a consistent choice is made throughout the library.
`ANNUAL` = annual, not sometimes annually sometimes yearly etc.
day_count is always day_count, not dc, day_count_convention, etc.

### 1.5 No defaults

Optional arguments?I prefer to have to specifically declare everything.
"Most interest rates are defined ACT/360" well no, so let's make sure
every single interest rate has the associated day count convention and 
compounding frequency.

## Definitions

### 1.1 Dates

We choose to implement dates using a new `Date` class rather than the default `datetime.date` from the 
standard library. Several reasons for that:

RelativeDelta, DateDelta, Term, Tenor, we choose `Period` because really is it just a period of time.
Easy instantiation: `Period("6M")` every knows this is 6 months.
Alternatively: `Period(6, Unit.MONTH)`, `Period(quantity=6, unit=Unit.MONTH)`, `Period(6, Unit("Month"))`,
`Period(6, "Month")`

Date(Y, M, D)
QuantLib defines as D, M, Y
American vs English are D, M, Y vs M, D, Y
it's confusing for everybody
The only format that is clear to everyone is Y M D since no one speaks in Y D M and neihter D nor M can 
have 4 digits.

### 1.2 Interest rates

Some definitions.

day count convention:

simple vs compounded. here, use the `Frequency` enum to specify the case.

spot rate = zero rate

Expressed in number, not percent or basis

So 5% is `Decimal("0.05")`, and a bp is `Decimal("0.0001")`

BusinessDayConvention, Adjustment, "Good Business Day", etc. MODIFIED_FOLLOWING

The `Calendar` object:
- holidays and business day adjustment are different concepts
- the calendar needs holidays (default is just weekends)
- adding days to a date taking holidays into account can't easily be done with operator overload, so need 
a dedicated `add` fonction in the Calendar object
- each `add` takes a convention into account because the convention is only used when adding days (or any period of 
  time) to a date, not when defining a calendar as such. A same calendar can be used with different conventions

calendar = Calendar(holidays="NYSE", convention=BusinessDayConvention.MODIFIED_FOLLOWING)
settlement_date = Calendar("NYSE").add(calculation_date, Days(2))

Markets MICs https://www.iso20022.org/market-identifier-codes

## Design goals

Simple and Pythonic API

I want to write: 

```python
start = Date.today()
end = start + Tenor("1M")
rate = 0.03
compounding = Compounding("Annually")
day_count = DayCount("ACT/360")

deposit = Deposit(
    start=start, 
    end=end, 
    rate=rate, 
    compounding=compounding, 
    day_count=day_count
)

cash_flows: list[CashFlow] = deposit.get_cashflows()

@total_ordering
class CashFlow:
    date: Date
    amount: Money
    
    # order by date

deposit = Deposit(start=Date(2023,9,18), maturity=Date(2023,10,18), rate=FixedInterestRate(0.03))
```

### Existing libraries

Quantlib: separation between evaluation date (set in global `ql.Settings` and curve which only contains
dates and values)