# Video-Compressor-Service
RecursionCSのBackendProject2_Video-Compressor-Serviceのリポジトリーになります。

## 概要
このサービスは動画を圧縮し、異なるフォーマットや解像度に変換することができるクライアントサーバ分散アプリケーションになります。

クライアントのホストシステムの代わりにサーバのリソースを使用することで、ユーザーはすべてのサービスを利用することができます。

TCP通信を用いてクライアント、サーバ間でデータの送受信を行い動画をサーバへアップロードしたり、

選択したサービスに基づき新しい動画をダウンロードできます。

サーバーサイドではFFMPEGライブラリを使用して、すべてのサービスを実現させています。

Video-Compressor-Service は以下のようなサービスを持ちます。
- 動画ファイルを圧縮する(圧縮度をlow,medium,highの3段階から選択できます)
- 動画の解像度を変更する
- 動画の縦横比を変更する
- 動画をオーディオに変換する
- 時間範囲からGIFを作成する


操作の流れは以下になります。

inputフォルダに動画を格納する

↓

CLI上で使用方法のコマンドを実行

↓

ユーザーは動画を選択

↓

クライアントからサーバへ動画をアップロードする

("Upload finish"が表示されるまで待つ)

↓

アップロードした動画に対してVideo-Compressor-Serviceのサービスを選択する

("File generated."が表示されるまで待つ)

↓

サービスを続けるか選択する

"0" : 終了する

"1" : 続ける

↓

outputフォルダにダウンロードされた動画を確認する

### client
![image](https://github.com/Aki158/Video-Compressor-Service/assets/119317071/8f96c6e0-80f9-48a1-9f17-0d5af6bffdfa)

### server
![image](https://github.com/Aki158/Video-Compressor-Service/assets/119317071/964ebb33-1094-4c8b-9c72-c0a7b7dad70a)

## output(すべてのサービスを実行後のフォルダ)
![image](https://github.com/Aki158/Video-Compressor-Service/assets/119317071/8a479707-2d84-4410-b7b1-5e49c66dd30c)

## サービス実施前後(例として サービス:動画ファイルを圧縮する_圧縮度_low をのせる)
### 実施前
![image](https://github.com/Aki158/Video-Compressor-Service/assets/119317071/ba663ead-75f0-4a92-b8aa-e4c469bc2680)

### 実施後
![image](https://github.com/Aki158/Video-Compressor-Service/assets/119317071/055507ac-fcac-4b7a-aac5-88b8c62fceec)

## 使用方法
### client
>python client.py

### server
>python3 server.py
