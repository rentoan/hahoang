# Python MT5 Trading Bot – Backtest to Forward-Test Pipeline

> **Portfolio Project – Simulated Client Requirement**

A modular Python trading automation project showing the path from deterministic strategy logic to paper forward-testing and an MT5 execution adapter.

## What This Project Demonstrates

- rule-based signal generation
- risk-based position sizing
- next-bar execution discipline
- one-position-at-a-time management
- SL / TP simulation
- trade logging
- paper forward-testing
- MT5 adapter structure
- Telegram-ready notifications
- operational checks before live deployment

## Architecture

```text
Market Data
    |
    v
Strategy Engine
    |
    v
Risk Engine
    |
    v
Execution Layer
   / \
  /   \
Paper  MT5 Adapter
Broker
  |
  v
Position Management
  |
  v
Trade Log + Notification
```

## Default Mode

```python
mode = "paper"
```

The repository is intentionally safe by default and does **not** send real orders.

## Strategy Used for the Demonstration

- Instrument style: XAUUSD / GOLD M30
- Long only
- Signal: Close above the highest High of the previous 20 bars
- Entry: next bar Open
- Stop: lowest Low of previous 10 bars including signal bar
- Target: 2R
- Risk: 1% of current equity
- One position at a time

The strategy exists only to demonstrate engineering. It is not presented as a profitable trading recommendation.

## Sample Paper Forward Result

- Bars processed: 1800
- Trades: 23
- Win rate: 43.5%
- Profit factor: 1.51
- Final equity: $10,696.93
- Max drawdown: 4.0%

Synthetic OHLC data is used in the repository.

## Project Structure

```text
project-07-python-mt5-backtest-forward-pipeline/
├── README.md
├── customer_requirements.txt
├── main.py
├── config/
│   └── settings.py
├── data/
│   └── xauusd_m30_sample.csv
├── src/
│   ├── strategy.py
│   ├── risk.py
│   ├── paper_broker.py
│   ├── mt5_broker.py
│   ├── forward_engine.py
│   ├── trade_logger.py
│   └── notifier.py
├── tests/
│   ├── test_strategy.py
│   └── test_risk.py
├── logs/
│   └── forward_trades.csv
├── reports/
│   └── Project07_Report.xlsx
└── screenshots/
```

## Run the Portfolio Demo

```bash
python main.py
```

No broker connection is required for paper mode.

## MT5 Integration

`src/mt5_broker.py` provides a thin adapter for the official `MetaTrader5` Python package.

A real client deployment must validate:

- broker symbol names
- minimum / maximum / step volume
- filling mode
- trading session availability
- spread / slippage assumptions
- broker retcodes
- terminal path and account login
- restart / reconciliation behavior

## Testing Philosophy

Trading automation should be treated as software engineering, not only strategy code.

The portfolio separates:

```text
strategy
risk
execution
logging
notification
broker integration
```

so each layer can be tested independently.

## Live Trading Warning

This repository is an engineering demonstration.

It does not guarantee profitability and should not be connected to a live trading account without broker-specific testing, forward testing, and risk review.
