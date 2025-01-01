import yfinance as yf
import pandas as pd


class DataFetcher:
    def __init__(self, query: str, period: str = "1d"):
        """
        株価データフェッチャーの初期化

        Args:
            query: 銘柄名または証券コード（例: "7203", "AAPL"）
            period: データ取得期間
        """
        self.query = query
        self.period = period
        self.ticker = self._resolve_ticker()

    def _resolve_ticker(self) -> str:
        """
        入力から適切なティッカーシンボルを解決する

        Returns:
            str: ティッカーシンボル
        """
        # 数字のみの場合は日本株の証券コードとして扱う
        if self.query.isdigit():
            return f"{self.query}.T"
        return self.query

    def fetch_ticker_info(self) -> yf.Ticker:
        """
        ティッカー情報を取得

        Returns:
            yf.Ticker: Tickerオブジェクト
        """
        ticker = yf.Ticker(self.ticker)
        return ticker

    def fetch_data_all(self) -> pd.DataFrame:
        """
        株価データを取得

        Returns:
            pd.DataFrame: 株価データ
        """
        data = yf.download(self.ticker, period=self.period)
        return data
