#!/bin/fish
# oj-prepare-open/hotarunx
# oj-prepareで指定した問題やコンテストに対し、
# テンプレートをVSCodeで開き、ブラウザで問題ページを開く

set templete_code_ext '.cpp' # 開くファイルの拡張子
set interval 60 # インターバル

set download_history ~/.cache/online-judge-tools/download-history.jsonl # ojの履歴ファイルのパス
set histories (tail -n100 $download_history) # 履歴ファイルのレコード最新100

set last_time (echo $histories[-1] | jq -r '.timestamp') # 最後の履歴のタイムスタンプ

# 履歴を走査する
for row in $histories
    # この履歴のタイムスタンプ
    set this_time (echo $row | jq -r '.timestamp')

    # この履歴と、最新の履歴の時間間隔がinterval未満のとき
    if test (math $last_time - $this_time) -le $interval
        # VSCodeで問題のテンプレートを開く
        find (echo $row | jq -r '.directory') -name '*'$templete_code_ext | xargs code
        # ブラウザで問題ページを開く
        open (echo $row | jq -r '.url')
    end
end
