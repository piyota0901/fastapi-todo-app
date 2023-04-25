# Todoアプリ
PythonのFastAPIを使用してRESTful APIを作成する

- FastAPI

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