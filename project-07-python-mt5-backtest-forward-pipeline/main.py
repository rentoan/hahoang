from pathlib import Path
import csv
import sys

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import BotConfig
from src.forward_engine import ForwardSimulationEngine
from src.trade_logger import TradeLogger
from src.notifier import TelegramNotifier

DATA_FILE = Path("data/xauusd_m30_sample.csv")
LOG_FILE = Path("logs/forward_trades.csv")


def load_bars(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    config = BotConfig()
    bars = load_bars(DATA_FILE)

    if config.mode != "paper":
        raise RuntimeError(
            "Portfolio main.py runs in paper mode. "
            "See src/mt5_broker.py for the live MT5 adapter."
        )

    engine = ForwardSimulationEngine(config)
    trades = engine.run(bars)

    TradeLogger(LOG_FILE).write_all(trades)

    notifier = TelegramNotifier()
    notifier.send(
        f"Portfolio07 finished: {len(trades)} trades. "
        f"Log: {LOG_FILE}"
    )

    print("Mode:", config.mode)
    print("Bars:", len(bars))
    print("Trades:", len(trades))
    print("Trade log:", LOG_FILE)


if __name__ == "__main__":
    main()
