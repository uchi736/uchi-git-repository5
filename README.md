# 高度RAGシステム (iRAG)

## 概要

本プロジェクトは、ドキュメント検索とSQL分析を融合させた高度なRAG（Retrieval-Augmented Generation）システムです。Streamlit製の洗練されたUIを備え、Azure OpenAI Serviceを活用して、アップロードされたドキュメントに対する自然言語での問い合わせや、構造化データ（CSV/Excel）に対するSQL分析を可能にします。

## 主な機能

- **ハイブリッド検索**: ベクトル検索とキーワード検索を組み合わせ、Reciprocal Rank Fusion (RRF) によって検索精度を向上させます。
- **日本語対応**: Janomeによる形態素解析を導入し、日本語のドキュメントに対しても高精度なキーワード検索を実現します。
- **Text-to-SQL**: 自然言語での質問を解釈し、アップロードされたCSV/Excelファイルから生成されたデータベーステーブルに対して自動的にSQLクエリを実行します。
- **専門用語辞書 (Golden-Retriever)**: ドキュメントから専門用語やその類義語を抽出し、辞書を自動構築。この辞書を用いてユーザーの質問を補強し、より的確な回答を生成します。
- **モジュール化されたUI**: 各機能（チャット、辞書、データ管理など）がタブごとにコンポーネント化されており、メンテナンスと拡張が容易です。

## ディレクトリ構造

リファクタリングにより、プロジェクトは機能ごとに明確に分割されました。

```
.
├── app.py                  # Streamlitアプリケーションのメインファイル
├── requirements.txt        # 必要なPythonパッケージ
├── .env.example            # 環境変数のテンプレート
├── rag/                    # RAGシステムのコアロジック
│   ├── __init__.py
│   ├── chains.py           # LangChainのプロンプトとチェーン定義
│   ├── config.py           # 設定クラス(Config)
│   ├── ingestion.py        # ドキュメントの取り込み・処理
│   ├── jargon.py           # 専門用語辞書の管理
│   ├── retriever.py        # ハイブリッド検索リトリーバー
│   ├── sql_handler.py      # Text-to-SQL関連の処理
│   └── text_processor.py   # 日本語テキスト処理
├── scripts/                # 独立したスクリプト
│   ├── term_extract.py
│   └── term_extractor_embeding.py
├── state.py                # Streamlitのセッション状態管理
├── ui/                     # UIコンポーネント
│   ├── __init__.py
│   ├── chat_tab.py
│   ├── data_tab.py
│   ├── dictionary_tab.py
│   ├── documents_tab.py
│   ├── settings_tab.py
│   └── sidebar.py
└── utils/                  # ユーティリティ関数・スタイル
    ├── __init__.py
    ├── helpers.py
    └── style.py
```

## セットアップ方法

1.  **仮想環境の作成と有効化**:
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # Linux/macOS
    myenv\Scripts\activate    # Windows
    ```

2.  **依存関係のインストール**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **環境変数の設定**:
    `.env.example` ファイルをコピーして `.env` ファイルを作成し、中身を自身の環境に合わせて編集します。最低限、以下の設定が必要です。
    - `AZURE_OPENAI_API_KEY`
    - `AZURE_OPENAI_ENDPOINT`
    - `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`
    - `AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME`
    - `PG_URL` (PostgreSQLの接続URL) または `DB_*` の各変数

## 実行方法

以下のコマンドでStreamlitアプリケーションを起動します。

```bash
streamlit run app.py
