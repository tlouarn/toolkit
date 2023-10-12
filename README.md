Different types of objets:

Quotes: trading levels like FixedRateDepositQuote, FixedFloatingInterestRateSwapQuote
Trades: actual trades like FixedRateDepositTrade, IndexFutureTrade, SingleStockForwardTrade


dates: dt.date
amounts: Money
holidays: HolidayBase

## Definitions

### 1.1 Dates

We choose to implement dates using a new `Date` class.

## Handling numbers

floats are fast but lack precisions
should we use Decimal for all calculations?


Difficulties with the terminology: a same concept can be named differently
by market practitioners. 

Conceptual difficulties: need to group conceptually-linked concepts together
e.g. an InterestRate can't be defined without a DayCount (or a Compounding)


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