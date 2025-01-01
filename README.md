# priceSeeker

一旦値動きを追う

## ファイル構造

project_root/
├── .uv/ # uv による環境管理ディレクトリ
├── .gitignore # Git で無視するファイルを指定
├── README.md # プロジェクトの概要と説明
├── requirements.txt # 依存パッケージの一覧
├── data/ # データファイルの保存場所
│ ├── raw/ # 生データ
│ └── processed/ # 処理済みデータ
├── src/ # ソースコードディレクトリ
│ ├── \_\_init\_\_.py # パッケージとして認識させるためのファイル
│ ├── data_fetcher.py # データ取得モジュール
│ ├── metadata_manager.py# メタデータ保存モジュール
│ ├── visualizer.py # データ可視化モジュール
│ └── app.py # Streamlit アプリのエントリーポイント
└── tests/ # テストコードディレクトリ
├── \_\_init\_\_.py
├── test_data_fetcher.py
├── test_metadata_manager.py
└── test_visualizer.py
