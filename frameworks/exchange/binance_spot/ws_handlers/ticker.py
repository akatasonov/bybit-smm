from typing import Dict

from frameworks.exchange.base.ws_handlers.ticker import Ticker, TickerHandler


class BinanceSpotTickerHandler(TickerHandler):
    def __init__(self, ticker: Ticker) -> None:
        super().__init__(ticker=ticker)

    def refresh(self, recv: Dict) -> None:
        try:
            self.ticker.update(
                fundingTime=0.0,
                fundingRate=0.0,
                markPrice=float(recv.get("price", self.ticker.markPrice)),
                indexPrice=float(recv.get("price", self.ticker.indexPrice)),
            )

        except Exception as e:
            raise Exception(f"Ticker refresh - {e}")

    def process(self, recv: Dict) -> None:
        try:
            self.ticker.update(
                fundingTime=float(recv.get("E", self.ticker.fundingTs)),
                fundingRate=0.0,
                markPrice=float(recv.get("c", self.ticker.markPrice)),
                indexPrice=float(recv.get("c", self.ticker.indexPrice)),
            )

        except Exception as e:
            raise Exception(f"Ticker process - {e}")
