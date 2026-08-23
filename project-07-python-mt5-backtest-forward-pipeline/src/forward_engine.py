from src.strategy import BreakoutStrategy
from src.risk import RiskEngine
from src.paper_broker import PaperBroker

class ForwardSimulationEngine:
    def __init__(self, config):
        self.config = config
        self.strategy = BreakoutStrategy(
            config.breakout_lookback,
            config.sl_lookback,
            config.rr
        )
        self.risk = RiskEngine(config.risk_pct)
        self.broker = PaperBroker()

    def run(self, bars):
        equity = self.config.initial_equity
        trades = []
        pending_signal = None
        trade_id = 0

        for i in range(len(bars)):
            bar = bars[i]

            # 1) manage existing position
            if self.broker.has_position():
                p = self.broker.position
                exit_result = self.broker.check_exit(bar)

                if exit_result:
                    risk_per_unit = p.entry - p.sl
                    r_multiple = (
                        (exit_result["exit_price"] - p.entry) / risk_per_unit
                        if risk_per_unit > 0 else 0
                    )
                    pnl = r_multiple * equity * self.config.risk_pct
                    equity += pnl

                    trade_id += 1
                    trades.append({
                        "TradeID": trade_id,
                        "SignalTime": pending_signal["signal_time"] if pending_signal else "",
                        "EntryTime": p.entry_time,
                        "ExitTime": bar["Time"],
                        "Side": p.side,
                        "Entry": round(p.entry, 2),
                        "SL": round(p.sl, 2),
                        "TP": round(p.tp, 2),
                        "Exit": round(exit_result["exit_price"], 2),
                        "Units": round(p.units, 4),
                        "RMultiple": round(r_multiple, 3),
                        "PnL": round(pnl, 2),
                        "EquityAfter": round(equity, 2),
                        "ExitReason": exit_result["reason"],
                    })
                    pending_signal = None

                continue

            # 2) execute signal from previous bar at current bar open
            if pending_signal:
                entry = float(bar["Open"])
                sl = float(pending_signal["stop_loss"])
                risk_per_unit = entry - sl

                if risk_per_unit > 0:
                    tp = entry + self.config.rr * risk_per_unit
                    units = self.risk.position_size_units(equity, entry, sl)
                    self.broker.open_buy(
                        bar["Time"], entry, sl, tp, units
                    )
                pending_signal = None
                continue

            # 3) detect new signal on closed bar
            signal = self.strategy.signal(bars, i)
            if signal:
                pending_signal = signal

        return trades
