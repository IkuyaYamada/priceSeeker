import streamlit as st
from src.data_fetcher import DataFetcher
import pandas as pd
import plotly.graph_objects as go

def add_base_trace(fig: go.Figure, data: pd.DataFrame) -> None:
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='終値'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Open'], mode='lines', name='始値'))
    fig.add_trace(go.Scatter(x=data.index, y=data['High'], mode='lines', name='高値'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Low'], mode='lines', name='安値'))

st.title("株価情報ビューワー")

# 銘柄入力フォーム
ticker_input = st.text_input(
    "銘柄コードまたはティッカーシンボルを入力してください",
    placeholder="例: 7203（トヨタ）, AAPL（アップル）",
    help="日本株は証券コード（4桁）、米国株はティッカーシンボルを入力してください"
)

if ticker_input:
    try:
        data_fetcher = DataFetcher(ticker_input)
        ticker_info = data_fetcher.fetch_ticker_info()
        nikkei_225 = DataFetcher("^n225").fetch_ticker_info()

        # 基本情報
        st.header("基本情報")
        info = ticker_info.info
        if info:
            st.write(info["longName"])
            st.write(info["longBusinessSummary"]) if "longBusinessSummary" in info else st.write("No summary available")
            on = st.toggle("詳細情報はこちら")
            if on:
                st.write(info)
            isJapan = info["currency"] == "JPY"
            currency = "¥" if isJapan else "$"
            col1, col2 = st.columns(2)
            with col1:
                st.metric("現在値", f"{currency}{info.get('currentPrice', 'N/A')}")
                try:
                    st.metric("始値", f"{currency}{info.get('open', 'N/A')}")
                except:
                    st.metric("始値", "N/A")
            with col2:
                try:
                    st.metric("時価総額", f"{currency}{info.get('marketCap', 'N/A'):,}")
                except:
                    st.metric("時価総額", "N/A")
                try:
                    st.metric("出来高", f"{currency}{info.get('volume', 'N/A'):,}")
                except:
                    st.metric("出来高", "N/A")

        # 株価チャート
        # 期間選択
        period_options = {
            "1日": "1d",
            "1週間": "1wk",
            "1ヶ月": "1mo",
            "3ヶ月": "3mo",
            "6ヶ月": "6mo",
            "1年": "1y",
            "2年": "2y",
            "5年": "5y",
            "最大": "max"
        }
        selected_period = st.selectbox(
            "期間を選択してください",
            options=list(period_options.keys()),
            index=2  # デフォルトで1ヶ月を選択
        )
        period = period_options[selected_period]
        st.header("株価チャート")
        history = ticker_info.history(period=period)
        history_225 = nikkei_225.history(period=period)

        # 通常の価格表示チャート
        fig = go.Figure()
        add_base_trace(fig, history)
        # 出来高を右のy軸として追加
        fig.add_trace(go.Scatter(
            x=history.index,
            y=history['Volume'],
            name='出来高',
            yaxis='y2',
        ))

        # レイアウト設定
        fig.update_layout(
            title="価格データと出来高",
            xaxis=dict(title="日付"),
            yaxis=dict(
                title="価格",
            ),
            yaxis2=dict(
                title="出来高",
                overlaying="y",
                side="right",
                tickformat=",d"  # カンマ区切りの整数表示
            ),
            legend=dict(x=0, y=1.1, orientation="h")
        )

        # 日経平均との比較チャート
        fig2 = go.Figure()
        add_base_trace(fig2, history)
        fig2.add_trace(go.Scatter(
            x=history_225.index,
            y=history_225['Close'],
            mode='lines',
            name='日経平均',
            yaxis='y2',
        ))
        fig2.update_layout(
            title="日経平均との比較",
            xaxis=dict(title="日付"),
            yaxis=dict(title="価格"),
            yaxis2=dict(
                title="日経平均",
                overlaying="y",
                side="right"
            ),
        )

        # 相対値での統合チャート
        st.header("相対値比較チャート")
        # 相対値の計算
        history_normalized = history.copy()
        history_225_normalized = history_225.copy()

        # 各データの開始日の値を100として正規化
        history_normalized['Close'] = history['Close'] / history['Close'].iloc[0] * 100
        history_normalized['Volume'] = history['Volume'] / history['Volume'].iloc[0] * 100
        history_225_normalized['Close'] = history_225['Close'] / history_225['Close'].iloc[0] * 100

        fig3 = go.Figure()

        # 株価（終値）
        fig3.add_trace(go.Scatter(
            x=history_normalized.index,
            y=history_normalized['Close'],
            mode='lines',
            name='終値',
        ))

        # 出来高
        # fig3.add_trace(go.Scatter(
        #     x=history_normalized.index,
        #     y=history_normalized['Volume'],
        #     mode='lines',
        #     name='出来高',
        # ))

        # 日経平均
        fig3.add_trace(go.Scatter(
            x=history_225_normalized.index,
            y=history_225_normalized['Close'],
            mode='lines',
            name='日経平均',
        ))

        # レイアウト設定
        fig3.update_layout(
            title="相対値比較（開始日=100）",
            xaxis=dict(title="日付"),
            yaxis=dict(title="相対値"),
            legend=dict(x=0, y=1.1, orientation="h")
        )

        # チャートの表示
        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)

        # アナリスト予想
        st.header("アナリスト予想")
        # st.write(ticker_info.analyst_price_targets)
        df = pd.DataFrame.from_dict(ticker_info.analyst_price_targets, orient='index', columns=['Value']).reset_index()
        st.dataframe(df)

        # 四半期決算
        st.header("四半期決算")
        st.dataframe(ticker_info.quarterly_income_stmt)

        # オプション情報
        if ticker_info.options:
            st.header("オプション情報")
            option_date = ticker_info.options[0]  # 最初の満期日
            st.write(f"満期日: {option_date}")
            st.dataframe(ticker_info.option_chain(option_date).calls)

    except Exception as e:
        st.error(f"データの取得に失敗しました: {str(e)}")
else:
    st.info("👆 銘柄を入力してください")
