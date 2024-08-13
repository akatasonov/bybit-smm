from frameworks.exchange.base.endpoints import Endpoint, Endpoints


class BinanceSpotEndpoints(Endpoints):
    def __init__(self) -> None:
        super().__init__()

        self.load_base(
            rest=Endpoint(url="https://api.binance.com", method="NONE"),
            public_ws=Endpoint(url="wss://stream.binance.com:443", method="NONE"),
            private_ws=Endpoint(url="wss://stream.binance.com:443", method="NONE"),
        )

        self.load_required(
            createOrder=Endpoint(url="/api/v3/order", method="POST"),
            amendOrder=Endpoint(url="/api/v3/order/cancelReplace", method="POST"),
            cancelOrder=Endpoint(url="/api/v3/order", method="DELETE"),
            cancelAllOrders=Endpoint(url="/api/v3/openOrders", method="DELETE"),
            getOrderbook=Endpoint(url="/api/v3/depth", method="GET"),
            getTrades=Endpoint(url="/api/v3/trades", method="GET"),
            getOhlcv=Endpoint(url="/api/v3/klines", method="GET"),
            getTicker=Endpoint(url="/api/v3/ticker/price", method="GET"),
            getOpenOrders=Endpoint(url="/api/v3/openOrders", method="GET"),
        )

        self.load_additional(
            ping=Endpoint(url="/api/v3/ping", method="GET"),
            exchangeInfo=Endpoint(url="/api/v3/exchangeInfo", method="GET"),
            accountInfo=Endpoint(url="/api/v3/account", method="GET"),
            listenKey=Endpoint(url="/api/v3/userDataStream", method="POST"),
            pingListenKey=Endpoint(url="/api/v3/userDataStream", method="PUT")
        )
