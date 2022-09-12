# oj-jordan

oj-prepare のラッパーツール。

## 機能

* `oj-prepare` のラッパー
* `oj-prepare` で指定した問題のページを開く
* `oj-prepare` が生成したテンプレートファイルを VSCode で開く
  * VSCode でファイルを編集して提出することを想定（提出ファイル）
* `oj-prepare` が生成した入力サンプルをコピーしたファイルを作成する
  * 標準入力リダイレクト先ファイルとして使用することを想定（標準入力リダイレクトファイル）
* `oj-prepare` が生成したファイル/ディレクトリのパスを渡すとその問題のページを開く

## How to install

git からパッケージをインストールしてください。

```shell
pip3 install git+https://github.com/hotarunx/oj-jordan.git
```

`.config/online-judge-tools/prepare.config.toml` の contest_directory problem_directory の値を下記に変更してください。

```toml
contest_directory = ""
problem_directory = "./{service_domain}/{contest_id}/{problem_id}"
```

## How to use

```shell
oj-jordan prepare URL
oj-jordan prepare URL [-c [CODING_FILE ...]]
oj-jordan browse PATH
```

詳細は `$ oj-jordan --help` を見てください。

### WSL

Web ページを Windows のブラウザで開くため、次のパッケージをインストールしてください。

```shell
sudo apt install wslu xdg-utils
```

### Windows, MacOS, Linux, Unix

テストしてません。

## Example

```shell
oj-jordan prepare https://atcoder.jp/contests/abc263/tasks/abc263_a -s test/in
oj-jordan prepare https://atcoder.jp/contests/abc264 -n 4 -c main.cpp main.py main.rs --config-file my.prepare.config.toml
oj-jordan browse atcoder.jp/abc263/abc263_a
oj-jordan prepare -h
oj-jordan browse -h
```

----------

## Note

[online\-judge\-tools](https://github.com/online-judge-tools) Organization とは無関係です。

## 主な使用モジュール

* [online\-judge\-tools/oj](https://github.com/online-judge-tools/oj)
* [online\-judge\-tools/api\-client](https://github.com/online-judge-tools/api-client)
* [online\-judge\-tools/template\-generator](https://github.com/online-judge-tools/template-generator)

## License

MIT License
