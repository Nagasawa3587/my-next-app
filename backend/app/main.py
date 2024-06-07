#FastAPIを使用してWebアプリケーションを構築する

#FastAPIのインポート
from fastapi import FastAPI

#CORSのインポート
#CORSMiddlewareは、FastAPIアプリケーションでCORS（Cross Origin Resource Sharing）を有効化するためのミドルウェアです。
#CORSは、Webアプリケーションが他のドメインからのリクエストを受け入れることを許可するためのものです。
from fastapi.middleware.cors import CORSMiddleware

#ルーターのインポート 　現在のディレクトリにあるtodo_router.py よりrouterをインポート
#クライアントからのリクエスト（例えば、WebページへのアクセスやAPIへのデータ要求）を受け取り、そのURLやHTTPメソッド（GET, POST, PUT, DELETEなど）に基づいて、どの関数を実行するかを決定します。
#ルーターは、FastAPIアプリケーションで定義されたエンドポイント（URL）に対応する関数を定義します。
from .todo_router import router as todo_router

#FastAPIアプリケーションのインスタンスを作成
#これにより、リクエストの管理、ルーティングの設定、ミドル
app = FastAPI()

#1. CORSミドルウェアの追加
#FastAPIアプリケーションにCORS（Cross-Origin Resource Sharing）ミドルウェアを追加し、異なるオリジン（ドメイン）からのリクエストを許可する設定が可能になります。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:3001"],  # フロントエンドのURL このURLのリクエストのみを許可する。
    allow_credentials=True, #認証情報（例えばクッキーやHTTP認証情報）を含むリクエストを許可
    allow_methods=["*"],  # すべてのHTTPメソッド（GET, POST, PUT, DELETEなど）を許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

#2. ルーターの組み込み
#todo_routerという名前でインポートされたルーターをアプリケーションに組み込みます。
#これにより、todo_routerで定義されたエンドポイント（URLとそれに対応する処理）がアプリケーションで利用可能になる。
app.include_router(todo_router)

#3. アプリケーションの実行
#このスクリプトが直接実行された場合にのみ、以下のコードが実行されます。
if __name__ == "__main__":
    #uvicornのインポート　uvicornは、インターネット上で私たちの作ったアプリケーションを動かすためのサーバーとして働きます。
    import uvicorn
    #アプリケーションをポート8000で実行します。
    uvicorn.run(app, host="0.0.0.0", port=8000)