from src.strategy import BreakoutStrategy

def test_no_signal_before_lookback():
    s = BreakoutStrategy(3, 2, 2.0)
    bars = [
        {"High":"1","Low":"0","Close":"1","Time":"a"},
        {"High":"2","Low":"1","Close":"2","Time":"b"},
    ]
    assert s.signal(bars, 1) is None

def test_breakout_signal():
    s = BreakoutStrategy(3, 2, 2.0)
    bars = [
        {"High":"10","Low":"8","Close":"9","Time":"a"},
        {"High":"11","Low":"9","Close":"10","Time":"b"},
        {"High":"12","Low":"10","Close":"11","Time":"c"},
        {"High":"14","Low":"11","Close":"13","Time":"d"},
    ]
    signal = s.signal(bars, 3)
    assert signal is not None
    assert signal["side"] == "BUY"
