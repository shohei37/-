# 本プログラムの目的：
# 「女の子一覧」ページのソースコードをもとに、
# 全デリヘル嬢のデータベースを作る

import bs4
import pandas as pd
import numpy as np
import re
import glob

# 有効な情報かどうかを判定
def is_valid_df(df):

    if( '割'            in df['名前'][0] or
        'コース'        in df['名前'][0] or
        '円'            in df['名前'][0] or
        'キャンペーン'  in df['名前'][0] or
        'ツイッター'    in df['名前'][0] or
        'LINE'          in df['名前'][0] or
        '日記'          in df['名前'][0]):
        return False
    if(df['年齢'][0] < 15 or 100 < df['年齢'][0]):
        return False
    if(df['バスト'][0] < 40 or 300 < df['バスト'][0]):
        return False
    if(df['ウエスト'][0] < 40 or 300 < df['ウエスト'][0]):
        return False
    if(df['ヒップ'][0] < 40 or 300 < df['ヒップ'][0]):
        return False
    
    # すべてのチェックをパスしたらTrueを返す
    return True

# 1行分のdataframeに変換する関数
def to_gal_df(gal_infos, prefecture, shop_name, shop_sub_info):

    # 1店舗分の女の子のdataframe
    gal_df_1shop = pd.DataFrame(
        index=[],
        columns=['名前',     '年齢',    '身長',
                 'バスト',   'カップ',  'ウエスト', 'ヒップ',
                 '一言説明', '都道府県', '店舗名',  '店舗種類']
    )

    for gal_info in gal_infos:

        # 1行分のdataframeを作る
        df = pd.DataFrame(
            index=[0],
            columns=['名前',     '年齢',    '身長',
                    'バスト',   'カップ',  'ウエスト', 'ヒップ',
                    '一言説明', '都道府県', '店舗名',  '店舗種類']
        )

        try:
            # split結果の例： ['', '咲歩(さほ)', '34歳／168cm／84(C)-58-87', '【敏感過ぎる身体】', ' 1', '']
            gal_info_split = gal_info.text.split('\n')

            # 名前の格納
            df['名前'][0] = gal_info_split[1]

            # 歳、身長、スリーサイズの格納
            # split後の例：['34歳', '168cm', '84', 'C', '', '58', '87']
            gal_spec = re.split('[／()-]', gal_info_split[2])
            df['年齢'][0]       = int(re.sub("\\D", "", gal_spec[0]))
            df['身長'][0]       = int(re.sub("\\D", "", gal_spec[1]))
            df['バスト'][0]     = int(gal_spec[2])
            # カップは書いている女の子と書いていない女の子がいるので処理分岐
            if(gal_spec[4] == ''):
                df['カップ'][0]     = gal_spec[3]
                df['ウエスト'][0]   = int(gal_spec[5])
                df['ヒップ'][0]     = int(gal_spec[6])
            else:
                df['カップ'][0]     = '-'
                df['ウエスト'][0]   = int(gal_spec[3])
                df['ヒップ'][0]     = int(gal_spec[4])

            # 一言説明
            df['一言説明'][0]   = gal_info_split[3]

            ### prefecture_infoの処理
            df['都道府県'][0]   = prefecture_info.text.strip()

            ### shop_name_infoの処理
            df['店舗名'][0]     = shop_name_info.text.strip()

            ### shop_sub_infoの処理
            shop_sub_info_split = re.split('[｜【]', shop_sub_info.text)
            shop_kind           = shop_sub_info_split[1].split(' ')
            df['店舗種類'][0]   = shop_kind[1]

            # 女の子のデータと判断したものはdataframeに追加
            if(is_valid_df(df)):
                gal_df_1shop = gal_df_1shop.append(df)
        
        # 配列に合わないデータになる場合は例外
        except:
            continue

    return gal_df_1shop


# ファイルリストを作る
file_paths = glob.glob('./htmls/*.html')

# 進捗確認用の変数
count_gals = 0
count_shops = 0
num_shops = len(file_paths)

# 空のdataframeを作る
gal_df = pd.DataFrame(
    index=[],
    columns=['名前',     '年齢',    '身長',
             'バスト',   'カップ',  'ウエスト', 'ヒップ',
             '一言説明', '都道府県', '店舗名',  '店舗種類']
)

for file_path in file_paths:

    # 対象のhtmlファイルからsoupを作成
    html = bs4.BeautifulSoup(open(file_path, encoding='utf-8'), 'html.parser')

    gal_infos       = html.find_all(class_="text")   # 女の子のスペックのみを取り出してリストにする
    prefecture_info = html.find(class_="logo")       # このタグの中に都道府県が書いてある
    shop_name_info  = html.find(class_="header_shop_title")  # このタグの中に店舗名が書いてある
    shop_sub_info   = html.find("title")    # このタグの中に店舗種類が書いてある(人妻デリヘルとか)

    # gal_infosから、1店舗分のdataframeを生成
    df = to_gal_df(gal_infos, prefecture_info, shop_name_info, shop_sub_info)

    #1店舗分のdfをgal_dfのケツに追加。最終的にはgal_dfをファイルに書き出す
    gal_df = gal_df.append(df)

    count_shops += 1
    print( '\r' + '現在 %04d / %04d 店舗目を処理中' % (count_shops, num_shops), end='' )

    # 100店舗ごとにgal_dfをファイル書き出し(途中でプログラムをストップしても中間結果が残るように)
    if(count_shops % 100 == 0):
        gal_df.to_csv("database/gals_database.csv", encoding='utf_8_sig', index=None)


# 最終結果をファイル書き出し
gal_df.to_csv("database/gals_database.csv", encoding='utf_8_sig', index=None)