from dataclasses import dataclass

@dataclass
class PaperPosition:
    side: str
    entry_time: str
    entry: float
    sl: float
    tp: float
    units: float

class PaperBroker:
    def __init__(self):
        self.position = None

    def has_position(self):
        return self.position is not None

    def open_buy(self, entry_time, entry, sl, tp, units):
        if self.position is not None:
            raise RuntimeError("Paper broker already has an open position.")

        self.position = PaperPosition(
            side="BUY",
            entry_time=entry_time,
            entry=entry,
            sl=sl,
            tp=tp,
            units=units,
        )
        return self.position

    def check_exit(self, bar):
        if self.position is None:
            return None

        p = self.position
        low = float(bar["Low"])
        high = float(bar["High"])

        # Conservative assumption for bar-based simulation:
        # if both SL and TP are inside the same candle, SL is assumed first.
        if low <= p.sl:
            result = {"exit_price": p.sl, "reason": "SL"}
        elif high >= p.tp:
            result = {"exit_price": p.tp, "reason": "TP"}
        else:
            return None

        self.position = None
        return result
