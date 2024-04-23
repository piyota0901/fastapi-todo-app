# 使い方

## 前提条件
- Poetry
- Docker
- Pyenv
- Node

## 環境構築(初回のみ)

### Backend

1. python 3.10.xのセットアップ
    ```bash
    $ pyenv install 3.10.13
    $ pyenv local 3.10.13
    ```

1. poetryの使用するPythonの設定
    ```bash
    $ poetry config virtualenvs.in-project true
    $ poetry env use python
    ```

1. ライブラリのインストール
    ```bash
    $ poetry install
    ```


## Frontend

1. npmモジュールのインストール
    ```bash
    $ cd frontend
    $ npm i
    ```

1. 
