Different types of objets:

Quotes: trading levels like FixedRateDepositQuote, FixedFloatingInterestRateSwapQuote
Trades: actual trades like FixedRateDepositTrade, IndexFutureTrade, SingleStockForwardTrade


dates: dt.date
amounts: Money
holidays: HolidayBase



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