# EasyTyping-Logger

[Easy タイピング（WebGL 版）](http://typingx0.net/easy/)からダウンロードされたタイピング結果画像を自動で読み取ります。  
読み取った結果を Google スプレッドシート上に出力します。

## 準備

- スプレッドシートにアプリの書き込み権限を与える

  - 参考：[Using OAuth2 for Authentication — gspread 3.1.0 documentation](https://gspread.readthedocs.io/en/latest/oauth2.html)
  - 参考： [【もう迷わない】Python でスプレッドシートに読み書きする初期設定まとめ | たぬハック ](https://tanuhack.com/operate-spreadsheet/)

- `.env`ファイルに設定を記述
  - ```
    CREDENTIAL_JSON_PATH=【認証情報jsonファイル】
    SPREADSHEET_KEY=【書き込むスプレッドシートのID】
    TARGET_DIR=【画像ダウンロード先フォルダ】
    ```
- 実行する
  - `python main.py`
