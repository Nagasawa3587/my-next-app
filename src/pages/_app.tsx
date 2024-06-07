// _app.tsx ファイルは、カスタム App コンポーネントのことで、アプリケーションの全ページに共通のレイアウトやページ間で状態を共有するための設定を行うNext.js関連のファイルです。
// ページがレンダリングされるたびに実行されるファイルです。

// グローバルなCSSファイルをインポート
import "@/styles/globals.css";

// Next.jsのAppProps型をインポート
// AppPropsは、Next.jsのアプリケーションに渡されるプロパティの型を定義したものです。Component: 現在アクティブなページを表す React コンポーネントです。pageProps:現在のページに渡されるデータです。
// next/appはモジュールでカスタムAPPコンポーネントを作成するための機能を提供する
import type { AppProps } from "next/app";

// App という名前の関数コンポーネントを定義しています。
//AppProps から Component と pageProps を抽出しています。
export default function App({ Component, pageProps }: AppProps) {
//抽出した Component をレンダリングし、そのコンポーネントに pageProps をプロパティとして渡しています。
//...pagePropsには、静的生成のデータ (getStaticProps)やサーバーサイドレンダリングのデータ (getServerSideProps)が含まれます。
  return <Component {...pageProps} />;
}
