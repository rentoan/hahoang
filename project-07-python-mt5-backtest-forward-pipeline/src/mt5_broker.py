class MT5Broker:
    """
    Thin adapter around the MetaTrader5 Python package.

    The portfolio runs in paper mode by default.
    To use this adapter on a machine with MT5 installed:
      1. pip install MetaTrader5
      2. open/login to MT5 terminal
      3. change config mode to "mt5"
      4. complete broker-specific symbol/volume settings
    """

    def __init__(self, symbol):
        self.symbol = symbol
        self.mt5 = None

    def connect(self):
        try:
            import MetaTrader5 as mt5
        except ImportError as e:
            raise RuntimeError(
                "MetaTrader5 package is not installed. Use paper mode or install MetaTrader5."
            ) from e

        if not mt5.initialize():
            raise RuntimeError(f"MT5 initialize() failed: {mt5.last_error()}")

        self.mt5 = mt5

    def shutdown(self):
        if self.mt5:
            self.mt5.shutdown()

    def has_position(self):
        positions = self.mt5.positions_get(symbol=self.symbol)
        return bool(positions)

    def open_buy(self, volume, sl, tp, magic=7007):
        tick = self.mt5.symbol_info_tick(self.symbol)
        if tick is None:
            raise RuntimeError("No MT5 tick available.")

        request = {
            "action": self.mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": volume,
            "type": self.mt5.ORDER_TYPE_BUY,
            "price": tick.ask,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": magic,
            "comment": "Portfolio07",
            "type_time": self.mt5.ORDER_TIME_GTC,
            "type_filling": self.mt5.ORDER_FILLING_IOC,
        }

        result = self.mt5.order_send(request)
        if result is None:
            raise RuntimeError("MT5 order_send returned None.")

        if result.retcode != self.mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(
                f"MT5 order failed retcode={result.retcode}, comment={result.comment}"
            )

        return result
