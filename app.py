# app.py
from flask import Flask, render_template
import numpy as np
from skyfield.api import Topos, load
from datetime import datetime, timezone

app = Flask(__name__)


@app.route("/")
def index():
    # 福岡の緯度経度
    fukuoka = Topos(latitude_degrees=33.5902, longitude_degrees=130.4017)

    # TLEをローカルファイルから読み込む
    tle_file_path = "gnss.txt"
    sats = load.tle_file(tle_file_path)
    # TLEを読み込む
    # sats = load.tle_file("https://celestrak.org/NORAD/elements/gnss.txt", reload=True)
    ts = load.timescale()

    # みちびき衛星のリスト
    michibiki_names = ["QZS-1R", "QZS-2", "QZS-3", "QZS-4"]
    michibiki_sats = {name: None for name in michibiki_names}

    # みちびき衛星を探す
    for sat in sats:
        for name in michibiki_names:
            if name in sat.name:
                michibiki_sats[name] = sat
                break

    # 現在の時刻を取得
    now = datetime.now(timezone.utc)  # 現在の時刻をUTCタイムゾーン付きで取得
    start_time = ts.utc(now.year, now.month, now.day, now.hour, now.minute, now.second)
    end_time = ts.utc(now.year, now.month, now.day + 7)  # 1週間後までを探索

    events_info = []

    for name, sat in michibiki_sats.items():
        if sat is not None:
            # 指定された時間範囲内で福岡の上空を通過するイベントを計算
            t, events = sat.find_events(
                fukuoka, start_time, end_time, altitude_degrees=10.0
            )

            # 次の通過イベントを探す
            for ti, event in zip(t, events):
                if event == 1:  # "culminate"（最高潮）イベント
                    events_info.append({"satellite": name, "time": ti.utc_datetime()})
                    break

    # ソートして最も近いイベントを先に表示
    events_info.sort(key=lambda x: x["time"])

    return render_template("index.html", events_info=events_info)


if __name__ == "__main__":
    app.run(debug=True)
