# oj-open

oj-prepareした後に問題をローカルで解く準備をするzshエイリアス。

ブラウザーでページを開くしVSCodeでmain.cppを開きます。
最初のサンプルを./test/debug.inにコピーする。デバッグの標準入力に使うことを想定している。

## Install

次のコマンドを実行してください。
一般的には`~/.zshrc`に追記します。

```shell
# https://github.com/hotarupoyo/oj-open
# oj-prepareした後に問題をローカルで解く準備をするzshエイリアス
# 1. ブラウザーで問題ページを開く
# 2. VSCodeでmain.cppを開く
# 3. 最初のサンプルを./test/debug.inにコピーする
oj-open () {
# 後でoj-prepare実行後の履歴を検索するためにタイムスタンプを取得する
ojo_timestamp=$(date +%s)

oj-prepare $1

# ブラウザーで問題ページを開く
jq -s '.' ~/.cache/online-judge-tools/download-history.jsonl | jq '[.[] | select(.timestamp > '$ojo_timestamp')]' | jq -r '.[].url' | head -n 6 | xargs -L 1 open
# VSCodeでmain.cppを開く
jq -s '.' ~/.cache/online-judge-tools/download-history.jsonl | jq '[.[] | select(.timestamp > '$ojo_timestamp')]' | jq -r '.[].directory' | head -n 6 | xargs -i code {}/main.cpp
# 最初のサンプルを./test/debug.inにコピーする
# デバッグの標準入力に使うことを想定した
jq -s '.' ~/.cache/online-judge-tools/download-history.jsonl | jq '[.[] | select(.timestamp > '$ojo_timestamp')]' | jq -r '.[].directory' | read -d '' ojo_dirs
ojo_dirs=(${(f)ojo_dirs})
for d in $ojo_dirs; do
    find ${d}/test/ -name '*.in' -type f | sort | head -n 1 | xargs -i cp {} ${d}/test/debug.in
done
}

# 昔oj-prepareした問題をローカルで解く準備をするzshエイリアス
oj-open-only () {
oj-api get-contest $1 | jq -r '.result.problems[].url' | read -d '' ojo_urls
ojo_urls=(${(f)ojo_urls})
for u in $ojo_urls; do
    jq -s '.' ~/.cache/online-judge-tools/download-history.jsonl | jq --arg u ${u} '[.[] | select(.url | contains($u))]' | jq -r '.[].url' | tail -n 1 | xargs -L 1 open
    jq -s '.' ~/.cache/online-judge-tools/download-history.jsonl | jq --arg u ${u} '[.[] | select(.url | contains($u))]' | jq -r '.[].directory' | tail -n 1 | xargs -i code {}/main.cpp
done
}
```

## How to use

```shell
oj-open URL
oj-open-only URL
oj-open https://kenkoooo.com/atcoder/#/contest/show/f14ba679-fc0a-4951-9989-209d176a0e56
oj-open-only https://kenkoooo.com/atcoder/#/contest/show/f14ba679-fc0a-4951-9989-209d176a0e56

```

---

## Note

[online\-judge\-tools](https://github.com/online-judge-tools) Organizationとは無関係です。

## 主な使用モジュール

- [online\-judge\-tools/oj](https://github.com/online-judge-tools/oj)
- [online\-judge\-tools/api\-client](https://github.com/online-judge-tools/api-client)
- [online\-judge\-tools/template\-generator](https://github.com/online-judge-tools/template-generator)

## License

MIT License
