from src.risk import RiskEngine

def test_position_size():
    r = RiskEngine(0.01)
    units = r.position_size_units(10000, 100, 95)
    assert abs(units - 20.0) < 1e-9

def test_invalid_stop():
    r = RiskEngine(0.01)
    assert r.position_size_units(10000, 100, 101) == 0
