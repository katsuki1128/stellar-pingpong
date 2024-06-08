# app.py
import matplotlib

matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import skyfield.api
from skyfield.framelib import itrs
from flask import Flask, render_template
import io
import base64
from matplotlib.animation import HTMLWriter

app = Flask(__name__)


@app.route("/")
def index():
    # TLEを読み込む
    sats = skyfield.api.load.tle_file(
        "https://celestrak.org/NORAD/elements/gnss.txt", reload=True
    )
    ts = skyfield.api.load.timescale()

    # QZS-1Rを探す
    qzs_1r = None
    for sat in sats:
        if "QZS-1R" in sat.name:
            qzs_1r = sat
            break

    if qzs_1r:
        # 時間設定
        time_range = ts.utc(2024, 6, 1, range(0, 24 * 60, 1))  # 1分ごとのデータ

        # 衛星の位置と速度を取得
        positions = [qzs_1r.at(t).frame_xyz(itrs).km for t in time_range]
        velocities = [qzs_1r.at(t).velocity.km_per_s for t in time_range]

        # 3Dプロットの設定
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        # 地球を球として描画
        # u = np.linspace(0, 2 * np.pi, 100)
        # v = np.linspace(0, np.pi, 100)
        # x = 6371 * np.outer(np.cos(u), np.sin(v))
        # y = 6371 * np.outer(np.sin(u), np.sin(v))
        # z = 6371 * np.outer(np.ones(np.size(u)), np.cos(v))

        # アニメーションの初期化
        def init():
            ax.clear()
            ax.set_xlim([-50000, 50000])
            ax.set_ylim([-50000, 50000])
            ax.set_zlim([-50000, 50000])
            ax.set_xlabel("X (km)")
            ax.set_ylabel("Y (km)")
            ax.set_zlabel("Z (km)")
            ax.set_title("QZS-1R (QZSS/PRN 196) Position and Velocity")
            return []

        # アニメーションの更新
        def update(frame):
            ax.clear()
            init()
            pos = positions[frame]
            vel = velocities[frame]
            scat = ax.scatter(pos[0], pos[1], pos[2], color="red", label="QZS-1R")
            quiv = ax.quiver(
                pos[0], pos[1], pos[2], vel[0], vel[1], vel[2], color="red"
            )
            # 軌跡を描く
            trajectory = np.array(positions[: frame + 1])
            ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color="red")
            return [scat, quiv]

        # アニメーションの作成
        ani = FuncAnimation(
            fig,
            update,
            frames=len(time_range),
            init_func=init,
            blit=False,
            interval=100,
        )

        # アニメーションの作成
        ani = FuncAnimation(
            fig,
            update,
            frames=len(time_range),
            init_func=init,
            blit=False,
            interval=100,
        )

        # アニメーションをHTMLに変換
        html_str = ani.to_html5_video()

        return render_template("index.html", animation_html=html_str)
    else:
        return "QZS-1R not found in the provided TLE data."


if __name__ == "__main__":
    app.run(debug=True)
