import asyncio
from typing import Tuple, Dict, List, Any

from frameworks.exchange.base.websocket import WebsocketStream
from frameworks.exchange.binance_spot.exchange import BinanceSpot
from frameworks.exchange.binance_spot.endpoints import BinanceSpotEndpoints
from frameworks.exchange.binance_spot.ws_handlers.orderbook import BinanceSpotOrderbookHandler
from frameworks.exchange.binance_spot.ws_handlers.trades import BinanceSpotTradesHandler
from frameworks.exchange.binance_spot.ws_handlers.ticker import BinanceSpotTickerHandler
from frameworks.exchange.binance_spot.ws_handlers.ohlcv import BinanceSpotOhlcvHandler
from frameworks.exchange.binance_spot.ws_handlers.orders import BinanceSpotOrdersHandler
from frameworks.exchange.binance_spot.ws_handlers.position import BinanceSpotPositionHandler


class DoNotProcess:
    """
    Placeholder class to indicate
    that the message should not be processed.
    """
    def __init__(self, *args, **kwargs):
        pass

    def process(self, *args, **kwargs):
        pass

class BinanceSpotWebsocket(WebsocketStream):
    """
    Handles Websocket connections and data management for Binance.
    """

    def __init__(self, exch: BinanceSpot) -> None:
        super().__init__()
        self.exch = exch
        self.endpoints = BinanceSpotEndpoints()

    def create_handlers(self) -> None:
        self.public_handler_map = {
            "depthUpdate": BinanceSpotOrderbookHandler(self.data["orderbook"]),
            "trade": BinanceSpotTradesHandler(self.data["trades"]),
            "kline": BinanceSpotOhlcvHandler(self.data["ohlcv"]),
            "24hrTicker": BinanceSpotTickerHandler(self.data["ticker"]),
        }
        self.public_handler_map["bookTicker"] = self.public_handler_map["depthUpdate"]

        self.private_handler_map = {
            "executionReport": BinanceSpotOrdersHandler(self.data["orders"], self.symbol),
            "outboundAccountPosition": DoNotProcess(), # do not need to handle this for now
        }

    async def refresh_orderbook_data(self, timer: int = 600) -> None:
        while True:
            try:
                orderbook_data = await self.exch.get_orderbook(self.symbol)
                self.public_handler_map["depthUpdate"].refresh(orderbook_data)
                await asyncio.sleep(timer)

            except Exception as e:
                await self.logging.warning(topic="WS", msg=f"orderbook: {e}")

    async def refresh_trades_data(self, timer: int = 600) -> None:
        while True:
            try:
                trades_data = await self.exch.get_trades(self.symbol)
                self.public_handler_map["trade"].refresh(trades_data)
                await asyncio.sleep(timer)

            except Exception as e:
                await self.logging.warning(topic="WS", msg=f"trades: {e}")

    async def refresh_ohlcv_data(self, timer: int = 600) -> None:
        while True:
            try:
                ohlcv_data = await self.exch.get_ohlcv(self.symbol, "1m")
                self.public_handler_map["kline"].refresh(ohlcv_data)
                await asyncio.sleep(timer)

            except Exception as e:
                await self.logging.warning(topic="WS", msg=f"ohlcv: {e}")

    async def refresh_ticker_data(self, timer: int = 600) -> None:
        while True:
            try:
                ticker_data = await self.exch.get_ticker(self.symbol)
                self.public_handler_map["24hrTicker"].refresh(ticker_data)
                await asyncio.sleep(timer)

            except Exception as e:
                await self.logging.warning(topic="WS", msg=f"ticker: {e}")

    def public_stream_sub(self) -> Tuple[str, List[Dict[str, Any]]]:
        request = [
            {
                "method": "SUBSCRIBE",
                "params": [
                    f"{self.symbol.lower()}@trade",
                    f"{self.symbol.lower()}@depth@100ms",
                    f"{self.symbol.lower()}@ticker",
                    f"{self.symbol.lower()}@kline_1m",
                ],
                "id": 1,
            }
        ]
        return (self.endpoints.public_ws.url, request)

    async def public_stream_handler(self, recv: Dict[str, Any]) -> None:
        try:
            self.public_handler_map[recv["e"]].process(recv)

        except KeyError as ke:
            if "id" not in recv:
                raise ke

        except Exception as e:
            raise e

    async def private_stream_sub(self) -> Tuple[str, List[Dict[str, Any]]]:
        listen_key_data = await self.exch.get_listen_key()
        listen_key = listen_key_data["listenKey"]
        url = self.endpoints.private_ws.url + "/ws/" + listen_key
        return (url, [])

    async def private_stream_handler(self, recv: Dict[str, Any]) -> None:
        try:
            self.private_handler_map[recv["e"]].process(recv)

        except KeyError as ke:
            if "listenKey" not in recv:
                raise ke

        except Exception as e:
            raise e

    async def ping_listen_key(self, timer: int = 1800) -> None:
        while True:
            try:
                await asyncio.sleep(timer)
                await self.exch.ping_listen_key()

            except Exception as e:
                await self.logging.error(topic="WS", msg=f"Pinging listen key: {e}")

    async def start_public_stream(self) -> None:
        """
        Initializes and starts the public Websocket stream.
        """
        try:
            url, requests = self.public_stream_sub()
            await self.start_public_ws(url, self.public_stream_handler, requests)
        except Exception as e:
            await self.logging.warning(topic="WS", msg=f"Public stream: {e}")

    async def start_private_stream(self) -> None:
        """
        Initializes and starts the private Websocket stream.
        """
        try:
            url, requests = await self.private_stream_sub()
            await self.start_private_ws(url, self.private_stream_handler, requests)
        except Exception as e:
            await self.logging.warning(topic="WS", msg=f"Private stream: {e}")

    async def start(self) -> None:
        self.create_handlers()
        await asyncio.gather(
            self.refresh_orderbook_data(),
            self.refresh_trades_data(),
            self.refresh_ohlcv_data(),
            self.refresh_ticker_data(),
            self.start_public_stream(),
            self.start_private_stream(),
            self.ping_listen_key(),
        )
