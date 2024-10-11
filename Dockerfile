# ベースイメージとしてPythonを指定
FROM python:3.11-slim

# 作業ディレクトリを作成
WORKDIR /app

# Pythonの依存関係を管理するためのファイルをコピー
COPY ./requirements.txt /app/requirements.txt

# 必要なPythonパッケージをインストール
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# アプリケーションのコードをコンテナ内にコピー
COPY ./app /app/app

# Uvicornを使ってFastAPIアプリを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
