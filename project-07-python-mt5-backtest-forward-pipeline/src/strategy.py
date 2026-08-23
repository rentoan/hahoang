class BreakoutStrategy:
    def __init__(self, breakout_lookback=20, sl_lookback=10, rr=2.0):
        self.breakout_lookback = breakout_lookback
        self.sl_lookback = sl_lookback
        self.rr = rr

    def signal(self, bars, i):
        if i < self.breakout_lookback:
            return None

        previous_high = max(
            float(x["High"])
            for x in bars[i-self.breakout_lookback:i]
        )

        if float(bars[i]["Close"]) <= previous_high:
            return None

        sl = min(
            float(x["Low"])
            for x in bars[max(0, i-self.sl_lookback):i+1]
        )

        return {
            "side": "BUY",
            "signal_index": i,
            "signal_time": bars[i]["Time"],
            "stop_loss": sl,
            "rr": self.rr,
        }
