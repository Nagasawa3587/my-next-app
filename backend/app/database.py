#SQLAlchemyを使用したデータベース操作の基礎を構築するためのもので、データベースとの接続、セッションの管理、およびモデル定義のための基本的なフレームワークを提供

#create_engine 関数をインポートします。これは、データベースエンジンを作成するために使用。
from sqlalchemy import create_engine
#declarative_base 関数をインポートします。これは、モデルクラスが継承するベースクラスを生成するために使用されます。
from sqlalchemy.ext.declarative import declarative_base
#sessionmaker 関数をインポートします。これは、セッションを作成するために使用されます。
from sqlalchemy.orm import sessionmaker

#2. データベースURLの設定:
#環境変数DATABASE_URLからデータベースのURLを取得します。URLが設定されていない場合はエラーログを出力し、ValueErrorを発生させます。
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://todo_user:Motoki21@localhost/todo_app"
#3. データベースエンジンの作成:
#create_engine関数を使用して、データベースエンジンを作成します。
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#4. セッションの作成:
#sessionmaker関数を使用して、セッションを作成します。
#autocommit=False は、DBへの変更を自動で反映しない。無効にすることを意味し、autoflush=False は、行った変更がすぐにデータベースに反映されないということです。
# bind=engine は、このセッションが使用するデータベースエンジンを指定する。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#5. デクララティブベースの生成:
#declarative_base関数を使用して、デクララティブベースを生成します。
#デクララティブベースは、モデルクラスが継承するベースクラスを生成します。
Base = declarative_base()

#お絵描きでいう「白い紙」のようなものです。お絵描きする前に紙が必要なように、データベースで情報をきちんと保存するためには、デクララティブベースが必要です。
#これがあるおかげで、私たちがデータベースに何を保存するか、どのように保存するかをきちんと決めることができ、情報を整理しておくことができます。
