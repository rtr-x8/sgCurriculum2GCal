# sgCurriculum2GCal

特定のフォーマットCSVからicsファイルに変換する。  

## usage

csv形式は`src/input_csv/input.sample.csv`を確認すること。  
読み込まれるCSVは`src/input_csv/input.csv`。

起動は以下のコマンドで動く。

```bash
docker compose up -d --build
```

出力されたICSファイルは`src/out`に出力される。unix時間がファイル名に入るので基本上書きされない。

CSVを読み込んでicsファイルを作成して、終了する。  
（ちょっとダサいけど放置）

