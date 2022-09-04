# oj-jordan

## Getting Started

git からパッケージをインストールしてください。

```shell
pip3 install git+https://github.com/hotarunx/oj-jordan.git
```

### WSL

Web ページを Windows のブラウザで開くため、次のパッケージをインストールしてください。

```shell
sudo apt install wslu xdg-utils
```

## for Developer

パッケージを editable モードでインストール。

```shell
pip3 install -e .
```

----------

## Memo

<https://atcoder.jp/contests/abc263/tasks/abc263_a>
<https://atcoder.jp/contests/abc263>

```shell
matikane@tanhauser [~](:|✔) % oj-api get-problem https://atcoder.jp/contests/abc263/tasks/abc263_a

INFO:onlinejudge_api.main:online-judge-api-client 10.10.0
INFO:onlinejudge_api.main:sleep 1.000000 sec
INFO:onlinejudge.utils:load cookie from: /Users/matikane/Library/Application Support/online-judge-tools/cookie.jar
INFO:onlinejudge._implementation.utils:network: GET: https://atcoder.jp/contests/abc263/tasks/abc263_a
INFO:onlinejudge._implementation.utils:network: 200 OK
INFO:onlinejudge._implementation.utils:network: GET: https://atcoder.jp/contests/abc263/tasks/abc263_a
INFO:onlinejudge._implementation.utils:network: 200 OK
INFO:onlinejudge._implementation.utils:network: GET: https://atcoder.jp/contests/abc263?lang=en
INFO:onlinejudge._implementation.utils:network: 200 OK
INFO:onlinejudge.utils:save cookie to: /Users/matikane/Library/Application Support/online-judge-tools/cookie.jar
{"status": "ok", "messages": [], "result": {"url": "https://atcoder.jp/contests/abc263/tasks/abc263_a", "tests": [{"input": "1 2 1 2 1\n", "output": "Yes\n"}, {"input": "12 12 11 1 2\n", "output": "No\n"}], "name": "Full House", "context": {"contest": {"name": "LINE  Verda Programming Contest\uff08AtCoder Beginner Contest 263\uff09", "url": "https://atcoder.jp/contests/abc263"}, "alphabet": "A"}, "memoryLimit": 1024, "timeLimit": 2000}}
```

```shell
matikane@tanhauser [~](:|✔) % oj-api get-contest https://atcoder.jp/contests/abc263/tasks/abc263_a

INFO:onlinejudge_api.main:online-judge-api-client 10.10.0
INFO:onlinejudge_api.main:sleep 1.000000 sec
INFO:onlinejudge.utils:load cookie from: /Users/matikane/Library/Application Support/online-judge-tools/cookie.jar
INFO:onlinejudge._implementation.utils:network: GET: https://atcoder.jp/contests/abc263?lang=en
INFO:onlinejudge._implementation.utils:network: 200 OK
INFO:onlinejudge._implementation.utils:network: GET: https://atcoder.jp/contests/abc263/tasks
INFO:onlinejudge._implementation.utils:network: 200 OK
INFO:onlinejudge.utils:save cookie to: /Users/matikane/Library/Application Support/online-judge-tools/cookie.jar
{"status": "ok", "messages": [], "result": {"url": "https://atcoder.jp/contests/abc263", "problems": [{"url": "https://atcoder.jp/contests/abc263/tasks/abc263_a", "name": "Full House", "context": {"contest": {"name": "LINE  Verda Programming Contest\uff08AtCoder Beginner Contest 263\uff09", "url": "https://atcoder.jp/contests/abc263"}, "alphabet": "A"}}, {"url": "https://atcoder.jp/contests/abc263/tasks/abc263_b", "name": "Ancestor", "context": {"contest": {"name": "LINE  Verda Programming Contest\uff08AtCoder Beginner Contest 263\uff09", "url": "https://atcoder.jp/contests/abc263"}, "alphabet": "B"}}, {"url": "https://atcoder.jp/contests/abc263/tasks/abc263_c", "name": "Monotonically Increasing", "context": {"contest": {"name": "LINE  Verda Programming Contest\uff08AtCoder Beginner Contest 263\uff09", "url": "https://atcoder.jp/contests/abc263"}, "alphabet": "C"}}, {"url": "https://atcoder.jp/contests/abc263/tasks/abc263_d", "name": "Left Right Operation", "context": {"contest": {"name": "LINE  Verda Programming Contest\uff08AtCoder Beginner Contest 263\uff09", "url": "https://atcoder.jp/contests/abc263"}, "alphabet": "D"}}, {"url": "https://atcoder.jp/contests/abc263/tasks/abc263_e", "name": "Sugoroku 3", "context": {"contest": {"name": "LINE  Verda Programming Contest\uff08AtCoder Beginner Contest 263\uff09", "url": "https://atcoder.jp/contests/abc263"}, "alphabet": "E"}}, {"url": "https://atcoder.jp/contests/abc263/tasks/abc263_f", "name": "Tournament", "context": {"contest": {"name": "LINE  Verda Programming Contest\uff08AtCoder Beginner Contest 263\uff09", "url": "https://atcoder.jp/contests/abc263"}, "alphabet": "F"}}, {"url": "https://atcoder.jp/contests/abc263/tasks/abc263_g", "name": "Erasing Prime Pairs", "context": {"contest": {"name": "LINE  Verda Programming Contest\uff08AtCoder Beginner Contest 263\uff09", "url": "https://atcoder.jp/contests/abc263"}, "alphabet": "G"}}, {"url": "https://atcoder.jp/contests/abc263/tasks/abc263_h", "name": "Intersection 2", "context": {"contest": {"name": "LINE  Verda Programming Contest\uff08AtCoder Beginner Contest 263\uff09", "url": "https://atcoder.jp/contests/abc263"}, "alphabet": "Ex"}}], "name": "LINE  Verda Programming Contest\uff08AtCoder Beginner Contest 263\uff09"}}
```

## 使用API

* [online\-judge\-tools/oj](https://github.com/online-judge-tools/oj)
* [online\-judge\-tools/api\-client](https://github.com/online-judge-tools/api-client)
* [online\-judge\-tools/template\-generator](https://github.com/online-judge-tools/template-generator)
