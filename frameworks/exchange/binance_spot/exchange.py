from typing import List, Dict, Optional

from frameworks.exchange.base.structures.order import Order
from frameworks.exchange.base.exchange import Exchange
from frameworks.exchange.binance_spot.endpoints import BinanceSpotEndpoints
from frameworks.exchange.binance_spot.formats import BinanceSpotFormats
from frameworks.exchange.binance_spot.client import BinanceSpotClient
from frameworks.exchange.binance_spot.orderid import BinanceSpotOrderIdGenerator

class BinanceSpot(Exchange):
    def __init__(self, api_key: str, api_secret: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret

        super().__init__(
            client=BinanceSpotClient(self.api_key, self.api_secret),
            formats=BinanceSpotFormats(),
            endpoints=BinanceSpotEndpoints(),
            orderIdGenerator=BinanceSpotOrderIdGenerator()
        )

    async def create_order(
        self,
        order
    ) -> Dict:
        endpoint = self.endpoints.createOrder
        headers = self.formats.create_order(order)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            data=self.client.sign_headers(endpoint.method, headers),
            signed=True,
        )

    async def batch_create_orders(
        self,
        orders: List[Order]
    ) -> Dict:
        endpoint = self.endpoints.batchCreateOrders
        headers = self.formats.batch_create_orders(orders)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            data=self.client.sign_headers(endpoint.method, headers),
            signed=True,
        )

    async def amend_order(
        self, order
    ) -> Dict:
        endpoint = self.endpoints.amendOrder
        headers = self.formats.amend_order(order)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            data=self.client.sign_headers(endpoint.method, headers),
            signed=True,
        )

    async def batch_amend_orders(
        self,
        orders: List[Order]
    ) -> Dict:
        endpoint = self.endpoints.batchAmendOrders
        headers = self.formats.batch_amend_orders(orders)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            data=self.client.sign_headers(endpoint.method, headers),
            signed=True,
        )

    async def cancel_order(self, order) -> Dict:
        endpoint = self.endpoints.cancelOrder
        headers = self.formats.cancel_order(order)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            data=self.client.sign_headers(endpoint.method, headers),
            signed=True,
        )

    async def batch_cancel_orders(
        self,
        orders: List[Order]
    ) -> Dict:
        endpoint = self.endpoints.batchCancelOrders
        headers = self.formats.batch_cancel_orders(orders)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            data=self.client.sign_headers(endpoint.method, headers),
            signed=True,
        )

    async def cancel_all_orders(self, symbol: str) -> Dict:
        endpoint = self.endpoints.cancelAllOrders
        headers = self.formats.cancel_all_orders(symbol)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            data=self.client.sign_headers(endpoint.method, headers),
            signed=True,
        )

    async def get_orderbook(self, symbol: str) -> Dict:
        endpoint = self.endpoints.getOrderbook
        params = self.formats.get_orderbook(symbol)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            params=params,
            signed=True,
        )

    async def get_trades(self, symbol: str) -> Dict:
        endpoint = self.endpoints.getTrades
        params = self.formats.get_trades(symbol)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            params=params,
            signed=True,
        )

    async def get_ohlcv(self, symbol: str, interval: str = "1m") -> Dict:
        endpoint = self.endpoints.getOhlcv
        params = self.formats.get_ohlcv(symbol, interval)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            params=params,
            signed=True,
        )

    async def get_ticker(self, symbol: str) -> Dict:
        endpoint = self.endpoints.getTicker
        params = self.formats.get_ticker(symbol)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            params=params,
            signed=True,
        )

    async def get_open_orders(self, symbol: str) -> Dict:
        endpoint = self.endpoints.getOpenOrders
        params = self.formats.get_open_orders(symbol)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            params=params,
            signed=True,
        )

    async def get_position(self, symbol: str) -> Dict:
        endpoint = self.endpoints.getPosition
        params = self.formats.get_position(symbol)
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            params=params,
            signed=True,
        )

    async def get_account_info(self) -> Dict:
        endpoint = self.endpoints.accountInfo
        params = self.formats.get_account_info()
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            params=params,
            signed=True,
        )

    async def get_exchange_info(self) -> Dict:
        endpoint = self.endpoints.exchangeInfo
        params = self.formats.get_exchange_info()
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            params=params,
            signed=True,
        )

    async def get_listen_key(self) -> Dict:
        endpoint = self.endpoints.listenKey
        params = self.formats.get_listen_key()
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            params=params,
            signed=True,
        )

    async def ping_listen_key(self) -> Dict:
        endpoint = self.endpoints.pingListenKey
        params = self.formats.ping_listen_key()
        return await self.client.request(
            url=self.base_endpoint.url + endpoint.url,
            method=endpoint.method,
            headers=self.client.base_headers,
            params=params,
            signed=True,
        )

    async def warmup(self) -> None:
        try:
            for symbol in (await self.get_exchange_info())["symbols"]:
                if self.symbol != symbol["symbol"]:
                    continue

                for filter in symbol["filters"]:
                    match filter["filterType"]:
                        case "PRICE_FILTER":
                            self.data["tick_size"] = float(filter["tickSize"])

                        case "LOT_SIZE":
                            self.data["lot_size"] = float(filter["stepSize"])

        except Exception as e:
            await self.logging.error(topic="EXCH", msg=f"Exchange warmup: {e}")

        finally:
            await self.logging.info(topic="EXCH", msg=f"Exchange warmup sequence complete.")
