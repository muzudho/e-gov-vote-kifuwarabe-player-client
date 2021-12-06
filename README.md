# e-gov-vote-kifuwarabe-player-client

電子政府きふわらべプレイヤー側クライアント（＾～＾）

📖 [AWSにデータベースサーバーってどうやって置くの（＾～＾）？](https://crieit.net/drafts/61890804402ea)  
📖 [e-gov-vote-kifuwarabe-server](https://github.com/muzudho/e-gov-vote-kifuwarabe-server)  

## Set up

```shell
# Test
python.exe -m pip install --index-url https://test.pypi.org/simple/ --no-deps state_machine_py

# Product
python.exe -m pip install state_machine_py
```

トップディレクトリに 📄`config.py` を作成し、内容を設定してください。  
内容は、以下のファイルを参考にしてください

Example:

📄`config--floodgate.py`
📄`config--local.py`

## Run

```shell
python.exe main.py
```

## Other documents

📖 [floodgate のログ](http://wdoor.c.u-tokyo.ac.jp/shogi/x/shogi-server.log)

![20211205shogi21a4.png](docs/img/20211205shogi21a4.png)  
👆 （WIP 書きかけ）むずでょの独自解釈の状態遷移図  
