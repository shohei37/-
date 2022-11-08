# 本プログラムの目的：
# 全店舗のトップページURLをもとに「女の子一覧」ページにアクセスし、
# 「女の子一覧」ページのソースを自分のPCにコピーする

import urllib.request
from urllib.error import URLError, HTTPError
import re
import time
import os

# 本プログラムは実行に時間がかかる。
# そのため、進捗をコンソール上に表示するための変数を用意
num_current = 0
num_shops = sum(1 for line in open('list/shop_list.txt'))

# 全店舗のトップページURLリストを開く
shop_top_urls = open('list/shop_list.txt', 'r')

for shop_top_url in shop_top_urls:

    shop_id = re.sub("\\D", "", shop_top_url)

    # 店舗のトップページのURLをもとに、
    # 「女の子一覧」ページのURLを生成
    # 例：https://s.dto.jp/shop/16721/gals
    gals_url = shop_top_url.strip() + '/' + 'gals'

    # 「女の子一覧」ページのhtmlを文字列で取得
    try:
        rf = urllib.request.urlopen(url=gals_url)
    except HTTPError as e:
        continue
    except URLError as e:
        continue
    tmp = rf.read()             # 「tmp」はbytes型の文字列になる
    html = tmp.decode("utf-8")  # str型に変換して変数「html」に格納
    rf.close()

    # URLから数字(店舗ID)を抜き出す。書き出しファイルの名前指定用。
    shop_id = re.sub("\\D", "", gals_url)
    # 書き出し先のファイルを作成。ファイル名は「htmls/(店舗ID).html」とする
    # 例：htmls/16721.html
    wf = open('htmls/' + shop_id + '.html', 'w', encoding='utf-8')

    # ファイルへの書き出し
    wf.write(html)
    wf.close()

    # デリヘルタウンのサーバに負荷をかけないよう、1回アクセスしたら2秒待つ
    time.sleep(2)

    # 現在何店舗取得したかをコンソール上に表示
    num_current += 1
    print( '\r' + '現在 %04d / %04d 店舗目を取得' % (num_current, num_shops), end='' )