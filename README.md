# image-to-text-search

画像内にある文字を検索します。  
あくまで補助的に利用し目視の確認を行ってください。  
特にsvgはpngに変換してからOCRをかけるため、検出精度が低い場合があります。  


## 実行方法

事前にDockerが必要


リポジトリをクローンしディレクトリに入る

```
$ cd image-to-text-search
```

`app/search_words.txt.sample` をコピーし`search_words.txt` を作成します。  
ファイル中に検索したい文字を記載します。  
（複数の場合は改行して追加）  


イメージをビルドします（search_words.txtやコードを変更した場合も再度ビルド）

```
$ docker build -t image-to-text-search .
```

下記を実行し画像内の検索したい文字がある画像を検索します

```
$ docker run --rm -it -v {ここに検索したいディレクトリのパスを記載}:/images image-to-text-search
```
