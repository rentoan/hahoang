# Project 06 – Python Trading Strategy Backtesting

Portfolio project demonstrating a reproducible **rule-based trading research and backtesting workflow**.

## Simulated Client Request

Backtest a simple XAUUSD M30 breakout strategy and deliver:

- reusable Python code
- trade-by-trade output
- performance metrics
- equity curve
- assumptions / limitations

## Strategy

- Long only
- Signal: Close above the highest High of the previous 20 bars
- Entry: next bar Open
- Stop: lowest Low of the previous 10 bars including signal bar
- Target: 2R
- Risk: 1% of current equity
- One open position at a time

## Pipeline

```text
Historical OHLC data
        ↓
Signal generation
        ↓
Trade simulation
        ↓
Risk-based P&L
        ↓
Trade log
        ↓
Performance metrics
        ↓
Excel report + equity curve
```

## Sample Result

This synthetic demonstration produced:

- Trades: 35
- Win rate: 37.1%
- Profit factor: 1.00
- Average R: 0.01
- Maximum drawdown: 7.2%
- Final equity: $10,006.76

These figures are **not trading claims**. The included OHLC data is synthetic.

## Files

```text
customer_requirements.txt
main.py
input/xauusd_m30_sample.csv
output/trades.csv
output/Backtest_Report.xlsx
screenshots/
```

## Important Backtest Assumptions

The report explicitly records assumptions that can materially change results, including same-bar SL/TP handling, entry timing, maximum holding period, and position sizing.

## Production Extensions

A client project could extend this foundation with:

- real broker/exchange historical data
- spread, commission, swap and slippage
- short trades
- parameter configuration
- walk-forward / out-of-sample analysis
- Monte Carlo / robustness testing
- MT5 integration
- paper trading / forward testing
- Telegram monitoring and execution logs

## Run

```bash
python main.py
```

Python standard library only.

## Portfolio Integrity

This project demonstrates backtesting engineering, not a profitable trading system.
No guarantee of future performance is made.
