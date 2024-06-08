# app.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import skyfield.api
from skyfield.framelib import itrs

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
    time_range = ts.utc(2024, 6, 1, range(0, 24 * 60, 1))  # 5分ごとのデータ

    # 衛星の位置と速度を取得
    positions = [qzs_1r.at(t).frame_xyz(itrs).km for t in time_range]
    velocities = [qzs_1r.at(t).velocity.km_per_s for t in time_range]

    # positionsリストの次元を確認
    # first_position = positions[0]
    # print(f"最初の位置データ: {first_position}")
    # print(f"最初の位置データの形状: {np.shape(first_position)}")
    # print(f"最初の位置データの次元: {len(first_position)}")
    # print(f"positionsリストの次元: {len(positions)}")

    # 3Dプロットの設定
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # 地球を球として描画
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 6371 * np.outer(np.cos(u), np.sin(v))
    y = 6371 * np.outer(np.sin(u), np.sin(v))
    z = 6371 * np.outer(np.ones(np.size(u)), np.cos(v))

    # 球の表面をプロット
    ax.plot_surface(x, y, z, color="b", alpha=0.6)

    # 軸ラベルの設定
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_zlabel("Z (km)")
    ax.set_title("Earth Sphere")

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

        # 球の表面を再描画
        ax.plot_surface(x, y, z, color="g", alpha=0.6)
        return []

    # アニメーションの更新
    def update(frame):
        # ax.clear()
        init()
        pos = positions[frame]
        vel = velocities[frame]
        scat = ax.scatter(pos[0], pos[1], pos[2], color="red", label="QZS-1R")
        quiv = ax.quiver(pos[0], pos[1], pos[2], vel[0], vel[1], vel[2], color="red")
        # 軌跡を描く
        trajectory = np.array(positions[: frame + 1])
        ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color="red")
        return [scat, quiv]

    # アニメーションの作成
    ani = FuncAnimation(
        fig, update, frames=len(time_range), init_func=init, blit=False, interval=100
    )

    #     # アニメーションをファイルに保存（5秒間の動画）
    #     # ani.save("japanese_satellites.mp4", writer="ffmpeg", fps=10)

    plt.legend()
    plt.show()
else:
    print("QZS-1R not found in the provided TLE data.")

# 日本製の衛星を探す
# japanese_sats = [sat for sat in sats if "QZS" in sat.name]

# if japanese_sats:
#     # 時間設定（1分ごとのデータ）
#     time_range = ts.utc(2024, 6, 1, range(0, 24 * 60, 1))  # 1分ごとのデータ

#     # 衛星の位置と速度を取得
#     positions = {
#         sat.name: [sat.at(t).frame_xyz(itrs).km for t in time_range]
#         for sat in japanese_sats
#     }
#     velocities = {
#         sat.name: [sat.at(t).velocity.km_per_s for t in time_range]
#         for sat in japanese_sats
#     }

#     # 3Dプロットの設定
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection="3d")

#     # 地球を球として描画
#     u = np.linspace(0, 2 * np.pi, 100)
#     v = np.linspace(0, np.pi, 100)
#     x = 6371 * np.outer(np.cos(u), np.sin(v))
#     y = 6371 * np.outer(np.sin(u), np.sin(v))
#     z = 6371 * np.outer(np.ones(np.size(u)), np.cos(v))

#     # アニメーションの初期化
#     def init():
#         ax.plot_surface(x, y, z, color="b", alpha=0.3)
#         ax.set_xlim([-50000, 50000])
#         ax.set_ylim([-50000, 50000])
#         ax.set_zlim([-50000, 50000])
#         ax.set_xlabel("X (km)")
#         ax.set_ylabel("Y (km)")
#         ax.set_zlabel("Z (km)")
#         ax.set_title("Japanese Satellites Position and Velocity")
#         return []

#     # アニメーションの更新
#     def update(frame):
#         # 以前のプロットデータをクリアする
#         # while ax.collections:
#         #     ax.collections.pop()
#         # while ax.lines:
#         #     ax.lines.pop()

#         # ax.plot_surface(x, y, z, color="b", alpha=0.3)

#         # 各衛星の位置と速度を描画
#         for sat_name in positions:
#             pos = positions[sat_name][frame]
#             vel = velocities[sat_name][frame]
#             scat = ax.scatter(pos[0], pos[1], pos[2], label=sat_name)
#             quiv = ax.quiver(pos[0], pos[1], pos[2], vel[0], vel[1], vel[2])

#             # 軌跡を描く
#             trajectory = np.array(positions[sat_name][: frame + 1])
#             ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2])

#         return []

#     # アニメーションの作成（intervalを100msに設定）
#     ani = FuncAnimation(
#         fig, update, frames=len(time_range), init_func=init, blit=False, interval=100
#     )

#     plt.legend()
#     plt.show()
# else:
#     print("No Japanese satellites found in the provided TLE data.")


# if qzs_1r:
#     # 現在の時刻
#     t = ts.now()

#     # 衛星の位置と速度を取得
#     geocentric = qzs_1r.at(t)
#     subpoint = geocentric.subpoint()
#     velocity = geocentric.velocity.km_per_s

#     print(f"QZS-1R（QZSS/PRN 196）の現在の位置と速度：")
#     print(f"緯度: {subpoint.latitude.degrees:.6f}°")
#     print(f"経度: {subpoint.longitude.degrees:.6f}°")
#     print(f"高度: {subpoint.elevation.km:.2f} km")
#     print(f"速度: {velocity}")

# else:
#     print("提供されたTLEデータにQZS-1Rが見つかりませんでした。")

# import skyfield.api

# # TLEを読み込む
# sats = skyfield.api.load.tle_file(
#     "https://celestrak.org/NORAD/elements/gnss.txt", reload=True
# )
# # 衛星が何個含まれているか？
# # print(len(sats))

# # 衛星が何個含まれているか？
# # print(f"Total satellites: {len(sats)}")

# # 全ての衛星の名前を列挙
# # print("All satellite names:")
# # for sat in sats:
# #     print(sat.name)

# # 日本の人工衛星を探す
# japanese_sats = [sat for sat in sats if "QZS" in sat.name]

# # 日本の人工衛星の名前を列挙
# print("Japanese satellites (QZSS):")
# for sat in japanese_sats:
#     print(sat.name)
# # みちびき衛星を探す
# # michibiki_sats = [sat for sat in sats if "Michibiki" in sat.name]

# # # みちびき衛星が見つかったか確認する
# # if michibiki_sats:
# #     print(f"Number of Michibiki satellites: {len(michibiki_sats)}")
# #     for idx, sat in enumerate(michibiki_sats):
# #         print(f"Michibiki Satellite {idx + 1}: {sat.name}")
# # else:
# #     print("No Michibiki satellites found.")

# # ts = skyfield.api.load.timescale()
# # sat = sats[0]

# # # 衛星の現在の位置を取得してみる
# # sat.at(ts.now())

# # <Geocentric ICRS position and velocity at date t center=399 target=-124876>

# # 座標を取得してみる
# print(sat.at(ts.now()).position)
# <Distance [-1.48650828e-04  2.47026029e-05  9.16709615e-05] au>

# # メートル単位で欲しい
# >>> sat.at(ts.now()).position.m
# array([-22229143.44338772,   3673091.13254689,  13733781.9073863 ])

# # 速度も得られる
# >>> sat.velocity.m_per_s
# array([ 1611.64563397, -2842.84923151,  2128.79653024])
