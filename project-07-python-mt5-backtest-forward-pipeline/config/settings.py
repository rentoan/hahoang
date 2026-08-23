from dataclasses import dataclass

@dataclass
class BotConfig:
    symbol: str = "GOLD"
    timeframe: str = "M30"

    breakout_lookback: int = 20
    sl_lookback: int = 10
    rr: float = 2.0

    risk_pct: float = 0.01
    initial_equity: float = 10000.0

    max_holding_bars: int = 120
    poll_seconds: int = 5

    # Portfolio safety default
    mode: str = "paper"  # paper | mt5
