# 本プログラムの目的：
# 「各地域の店舗リスト」をもとにして、
# 全登録店舗のURLを取得する

from requests_html import HTMLSession
import re
import time

# 本プログラムは実行に時間がかかる。
# そのため、進捗をコンソール上に表示するための変数を用意
num_current = 0
num_shops = sum(1 for line in open('list/area_list.txt'))

# デリヘルタウントップのURL
url_dto = 'https://www.dto.jp'

# get_area_listで作った各地域の店舗リスト
rf = open('list/area_list.txt', 'r')

# 以下、全店舗のURLをリストに詰め込む
shop_list = []
for line in rf:

    # 店舗リストから各店舗のURL取得
    session = HTMLSession()
    r = session.get(line.strip())

    for link in r.html.links:
        # 取得したURLから、店舗のURLだけ選別して書き出す。
        # 取得するURLの例：「/shop/30552」とか「/shop/29517」とか
        is_shop = re.search('/shop/', link)
        if(is_shop):
            # https://www.dto.jp/を頭につけてリストに追加
            shop_list.append(url_dto + link)
    
    # サーバに負荷をかけないよう、1つのページにアクセスするごとに1秒停止
    time.sleep(1)

    # 現在の進捗を表示
    num_current += 1
    print( '\r' + '現在の進捗： %03d / %03d ' % (num_current, num_shops), end='' )


# 以下、ファイルへの書き出し

# shop_listには、店舗のURLを片っ端からぶち込んでいる。よってURLが重複していることがある。
# そのため、setコマンドによって重複をなくす。
shop_list = list(set(shop_list))

# 書き出し先のファイル
wf = open('list/shop_list.txt', 'w')

# リストをファイルに書き出し
for shop in shop_list:
    wf.write(shop + '\n')