from src.data_fetcher import DataFetcher
import pytest


def test_data_fetcher_us_stock():
    data_fetcher = DataFetcher("AAPL")
    data = data_fetcher.fetch_data_all()
    assert data is not None
    assert not data.empty

def test_data_fetcher_jp_stock():
    data_fetcher = DataFetcher("7203")  # トヨタ自動車
    data = data_fetcher.fetch_data_all()
    assert data is not None
    assert not data.empty

def test_ticker_resolution():
    # 日本株のケース
    jp_fetcher = DataFetcher("7203")
    assert jp_fetcher.ticker == "7203.T"

    # 米国株のケース
    us_fetcher = DataFetcher("AAPL")
    assert us_fetcher.ticker == "AAPL"
