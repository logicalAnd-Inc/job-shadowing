# job-shadowing
職場体験用 flask+sqliteアプリケーション

## 環境構築
1. git clone

2. `docker-compose.yml` の `context` が以下のようになっていることを確認します。
    ```yaml
    version: '0'

    services:
    web:
        build: .
        ports:
        - '8888:5000'
        volumes:
        - ./app:/app
    ```

3. コンテナをビルドします。

    ```
    docker-compose up
    ```

4. [トップページ](http://localhost:8888) にアクセスし、画面が表示されることを確認します。