class RiskEngine:
    def __init__(self, risk_pct):
        self.risk_pct = risk_pct

    def risk_amount(self, equity):
        return equity * self.risk_pct

    def position_size_units(self, equity, entry, stop_loss):
        risk_per_unit = entry - stop_loss
        if risk_per_unit <= 0:
            return 0.0
        return self.risk_amount(equity) / risk_per_unit
