`python cobra.py [問題番号] [-p]`  
上記のコマンドで指定問題を画像復元し、ローカルサーバーが立ち上がります。A-star/以下の実行ファイルがアクセスすると画像復元結果をhttp通信で返答します。  

-pをつけなければsp2lc.salesio-sp.ac.jpと通信します。問題番号は http://sp2lc.salesio-sp.ac.jp に接続して確認してね。  
-dを付けるとどこにも解答を送信しません。  
-nを付けるとウィンドウを表示しません。SSH越しでの実行などにどうぞ。  
-rで沖縄高専の練習場と通信します。  


config.py内の情報を書き換えることで-pを利用したときの回答サーバーのipを指定できます。  


試合が始まったらEnterキーを押して画像認識を開始してください。


`pypy ***.py [cobraのip]`  
回答探査プログラムを実行します。cobra.pyから画像復元結果が取得できるときのみ動作します。  
config.pyを書き換えることでcobra.pyが駆動してるサーバーのipを常時指定できます。その場合オプションは必要ありません。  
`pypy L.py [cobraのip] [縮小先columns-縮小先rows]`  
`L.py`と`L-good.py`に関しては縮小先マス数を引数で指定できます。  
その場合 - で区切った一連の文字列で指定してください。 ex`pypy L-good.py 5-5`  


