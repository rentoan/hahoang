import csv
from pathlib import Path

class TradeLogger:
    FIELDS = [
        "TradeID","SignalTime","EntryTime","ExitTime",
        "Side","Entry","SL","TP","Exit",
        "Units","RMultiple","PnL","EquityAfter","ExitReason"
    ]

    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write_all(self, rows):
        with self.path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS)
            writer.writeheader()
            writer.writerows(rows)
