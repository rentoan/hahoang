from pathlib import Path
import csv

DATA = Path("input/xauusd_m30_sample.csv")
OUTPUT = Path("output/trades.csv")
LOOKBACK = 20
SL_LOOKBACK = 10
RR = 2.0
RISK_PCT = 0.01
INITIAL_CAPITAL = 10000.0

def load_bars(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def f(row, key):
    return float(row[key])

def backtest(bars):
    equity = INITIAL_CAPITAL
    trades = []
    i = LOOKBACK

    while i < len(bars) - 1:
        previous_high = max(f(x, "High") for x in bars[i-LOOKBACK:i])

        if f(bars[i], "Close") > previous_high:
            entry_i = i + 1
            entry = f(bars[entry_i], "Open")
            sl = min(f(x, "Low") for x in bars[max(0, i-SL_LOOKBACK):i+1])
            risk = entry - sl

            if risk > 0.5:
                tp = entry + RR * risk
                exit_i = None
                exit_price = None

                for j in range(entry_i, min(len(bars), entry_i + 120)):
                    # Conservative assumption if SL and TP are both touched in one bar.
                    if f(bars[j], "Low") <= sl:
                        exit_i, exit_price = j, sl
                        break
                    if f(bars[j], "High") >= tp:
                        exit_i, exit_price = j, tp
                        break

                if exit_i is None:
                    exit_i = min(len(bars)-1, entry_i+119)
                    exit_price = f(bars[exit_i], "Close")

                r_multiple = (exit_price-entry)/risk
                pnl = equity * RISK_PCT * r_multiple
                before = equity
                equity += pnl

                trades.append({
                    "TradeID": len(trades)+1,
                    "EntryTime": bars[entry_i]["Time"],
                    "ExitTime": bars[exit_i]["Time"],
                    "Entry": round(entry, 2),
                    "SL": round(sl, 2),
                    "TP": round(tp, 2),
                    "Exit": round(exit_price, 2),
                    "RMultiple": round(r_multiple, 3),
                    "PnL": round(pnl, 2),
                    "EquityBefore": round(before, 2),
                    "EquityAfter": round(equity, 2),
                })

                i = exit_i + 1
                continue
        i += 1
    return trades

def save(rows):
    OUTPUT.parent.mkdir(exist_ok=True)
    if not rows:
        return
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    bars = load_bars(DATA)
    trades = backtest(bars)
    save(trades)
    print("Bars:", len(bars))
    print("Trades:", len(trades))
    print("Output:", OUTPUT)
