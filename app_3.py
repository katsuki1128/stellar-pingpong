import numpy as np
from skyfield.api import Topos, load
from datetime import datetime, timedelta, timezone

# 福岡の緯度経度
fukuoka = Topos(latitude_degrees=33.5902, longitude_degrees=130.4017)

# TLEを読み込む
sats = load.tle_file("https://celestrak.org/NORAD/elements/gnss.txt", reload=True)
ts = load.timescale()

# QZS-1Rを探す
qzs_1r = None
for sat in sats:
    if "QZS-1R" in sat.name:
        qzs_1r = sat
        break

if qzs_1r:
    # 現在の時刻を取得
    now = datetime.now(timezone.utc)  # 現在の時刻をUTCタイムゾーン付きで取得
    start_time = ts.utc(now.year, now.month, now.day, now.hour, now.minute, now.second)
    end_time = ts.utc(now.year, now.month, now.day + 7)  # 1週間後までを探索

    # 指定された時間範囲内で福岡の上空を通過するイベントを計算
    t, events = qzs_1r.find_events(fukuoka, start_time, end_time, altitude_degrees=10.0)

    # 次の通過イベントを探す
    next_event_time = None
    for ti, event in zip(t, events):
        if event == 1:  # "culminate"（最高潮）イベント
            next_event_time = ti
            break

    if next_event_time is not None:
        # 現在の時刻と次の通過時刻の差を計算
        time_difference = next_event_time.utc_datetime() - now
        print(f"次に福岡の真上を通過するまでの時間: {time_difference}")
        print(f"通過時刻: {next_event_time.utc_datetime()} UTC")
    else:
        print("次の1週間以内に福岡の真上を通過するイベントが見つかりませんでした。")
else:
    print("QZS-1R not found in the provided TLE data.")
