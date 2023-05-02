# Todoアプリ
PythonのFastAPIを使用してRESTful APIを作成する

- FastAPI


## 参考になるリポジトリ

[Full-Stack-FastAPI-PostgreSQL](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D)

## 対話的APIドキュメント
[Swagger UI](http://127.0.0.1:8000/docs)
[Redoc](http://127.0.0.1:8000/redoc)

## ヘルスチェック
https://testfully.io/blog/api-health-check-monitoring/

## デバッグ
VS Codeの`launch.json`に以下を設定してデバッグ
<details>
    <summary>launch.json</summary>

    ```json
    {
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            // "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "module": "uvicorn",
            "args": [
                "todo_app.main:app",
                "--reload"
                ]
            }
        ]
    }
    ```
</details>

[参考](https://zenn.dev/kazukinoto/scraps/0ef097372a5aa0)

## Python
- `****.pyc`が生成されないようにする
  - `PYTHONDONTWRITEBYTECODE=1`を設定する

## FastAPI
- `BaseModel`の`orm_mode=True`
  - ORMのオブジェクトをPydanticのレスポンスオブジェクトに自動的に変換してくれる
    - 何がうれしいか ⇒ パスオペレーションのCRUDで、DBから取得したオブジェクト(orm_mode=True)を
    returnしても自動的にPydanticのモデルになってくれる

## SQLAlchemy


### モデル定義
Postgresqlのカラムがある
https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-data-types

- UUID
  - https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy
  - 上記で行けるかと思ったけどうまくいかなかった
  - `sqlalchemy-utils`を使用してUUIDを設定
- 


## Alembic
- データ登録したい場合
  - `bulk insert`を使う
    ```python
    from alembic import op
    from datetime import date
    from sqlalchemy.sql import table, column
    from sqlalchemy import String, Integer, Date

    # Create an ad-hoc table to use for the insert statement.
    accounts_table = table(
        "account",
        column("id", Integer),
        column("name", String),
        column("create_date", Date),
    )

    op.bulk_insert(
        accounts_table,
        [
            {
                "id": 1,
                "name": "John Smith",
                "create_date": date(2010, 10, 5),
            },
            {
                "id": 2,
                "name": "Ed Williams",
                "create_date": date(2007, 5, 27),
            },
            {
                "id": 3,
                "name": "Wendy Jones",
                "create_date": date(2008, 8, 15),
            },
        ],
    )
    ```
### Trouble Shooting
- `alembic revision --autogenerate -m "XXXXX"`で以下のエラーが出た場合
    ```bash
    INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
    INFO  [alembic.runtime.migration] Will assume transactional DDL.
    ERROR [alembic.util.messaging] Target database is not up to date.
    FAILED: Target database is not up to date.
    ```
    - 原因
        - 過去のrevisionが存在していてupgradeしていないことが原因
    - 対処方法
        - `poetry run alembic upgrade head`コマンドを実行して最新にする
        - その後、`alembic revision --autogenerate -m "XXXXX"`を実行する。

- `postgresql`に繋がらず`peer`認証のエラーが出る場合
    ```bash
    psql --username todo_app --dbname tododb
    psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  Peer authentication failed for user "todo_app"
    ```
    - 原因
        `/etc/postgresql/15/main/pg_hba.conf`の設定でpeerとなっていることが原因らしい
    - 対処方法
        1. `sudo vim  /etc/postgresql/15/main/pg_hba.conf`
        2. `local  all    all   peer` -> `local  all    all   md5`に変更
        3. `sudo service postgresql restart`

- `alembic`で過去のrevisionを消したいとき
  - 正式なやり方は不明だが、以下の流れ。
  - 1. `alembic downgrade base` もしくは指定のrevisionまでdowngradeさせる。
  - 2. `version`フォルダ配下のrevisionファイルを削除する。


- `base_class.py`の`Base`を読み込ませると`alembic`に反映されない
  - importの関係でBaseだけ読み込んでしまいBaseを継承しているmodelが読み込まれていない
  - なので`base_class.py`を作成してBaseクラスを定義
  - `base.py`でBaseクラスと、Baseクラスを継承したクラスをimportする。⇒これにより、Baseを読みだしたときBaseを継承しているmodelがBaseのmetadataに含まれるようになる。