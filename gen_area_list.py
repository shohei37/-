# 本プログラムの目的：
# デリヘルタウンのトップページにある、
# 「各地域の店舗リスト」のURLをファイルに書き出す

from requests_html import HTMLSession
import re

# デリヘルタウントップのURL
url_dto = 'https://www.dto.jp'

# デリヘルタウントップページの情報取得
session = HTMLSession()
r = session.get(url_dto)

# 以下、ファイルへの書き出し
f = open('list/area_list.txt', 'w')
for link in r.html.links:

    # 取得したURLから、都道府県を表すURLだけ選別して書き出す。

    # 取得するURLの例：「/hokkaido」とか「/aomori」とか。スラッシュの数で判別する
    is_main_area = ( len(link.split('/')) == 2 )
    if(is_main_area):
        # https://www.dto.jp/を頭につけてファイル書き出し
        f.write(url_dto + link + '/shop-list' + '\n')
    
    # 取得するURLの例：「/mito/shop-list」とか「/hakata/shop-list」とか
    is_sub_area = re.search('/*/shop-list', link)
    if(is_sub_area):
        # https://www.dto.jp/を頭につけてファイル書き出し
        f.write(url_dto + link + '\n')

