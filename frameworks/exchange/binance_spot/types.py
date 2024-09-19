from frameworks.exchange.base.constants import PositionDirectionConverter, SideConverter, TimeInForceConverter, OrderTypeConverter


class BinanceSideConverter(SideConverter):
    def __init__(self) -> None:
        super().__init__(
            BUY="BUY",
            SELL="SELL"
        )

class BinanceOrderTypeConverter(OrderTypeConverter):
    def __init__(self) -> None:
        super().__init__(
            LIMIT="LIMIT",
            MARKET="MARKET",
            STOP_LIMIT="STOP",
            TAKE_PROFIT_LIMIT="TAKE_PROFIT",
            POST_ONLY="LIMIT_MAKER"
        )

class BinanceTimeInForceConverter(TimeInForceConverter):
    def __init__(self) -> None:
        super().__init__(
            GTC="GTC",
            IOC="IOC",
            FOK="FOK"
        )

class BinancePositionDirectionConverter(PositionDirectionConverter):
    def __init__(self) -> None:
        super().__init__(
            LONG="LONG",
            SHORT="SHORT"
        )