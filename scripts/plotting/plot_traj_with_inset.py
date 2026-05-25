#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch


# =========================
# 可调样式参数（细线版）
# =========================
FIG_W, FIG_H = 14, 6
DPI = 220

TRAJ_LW_GT = 1.0
TRAJ_LW_EST = 1.0
BOX_LW = 1.5
LINK_LW = 1.0

GT_COLOR = "0.45"
VINS_COLOR = "#4C72B0"
DR_COLOR = "#55A868"
BOX_COLOR = "red"
LINK_COLOR = "#4A90E2"

LABEL_FS = 14
TICK_FS = 11
LEGEND_FS = 11
TITLE_FS = 16


# =========================
# 读取 TUM 轨迹
# 每行格式:
# t x y z qx qy qz qw
# 也兼容逗号分隔
# =========================
def load_tum(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")

    ts = []
    xyz = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [x for x in line.replace(",", " ").split() if x]
            if len(parts) < 8:
                continue

            try:
                t = float(parts[0])
                # 若是纳秒时间戳，则转成秒
                if t > 1e12:
                    t /= 1e9

                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])

                ts.append(t)
                xyz.append([x, y, z])
            except ValueError:
                continue

    if len(ts) == 0:
        raise RuntimeError(f"没有从文件中读取到有效轨迹点: {path}")

    ts = np.asarray(ts, dtype=np.float64)
    xyz = np.asarray(xyz, dtype=np.float64)

    # 按时间排序
    order = np.argsort(ts)
    ts = ts[order]
    xyz = xyz[order]

    return ts, xyz


# =========================
# 轨迹时间戳关联
# 以 ref 为基准，为每个 ref 点找最近的 est 点
# =========================
def associate_by_timestamp(ts_ref, xyz_ref, ts_est, xyz_est, max_diff=0.05):
    i, j = 0, 0
    matched_ref = []
    matched_est = []

    while i < len(ts_ref) and j < len(ts_est):
        dt = ts_ref[i] - ts_est[j]

        if abs(dt) <= max_diff:
            matched_ref.append(xyz_ref[i])
            matched_est.append(xyz_est[j])
            i += 1
            j += 1
        elif dt > 0:
            j += 1
        else:
            i += 1

    if len(matched_ref) < 3:
        return None, None

    return np.asarray(matched_ref), np.asarray(matched_est)


# =========================
# Umeyama 对齐（默认不估计尺度）
# 求 src -> dst
# =========================
def umeyama_alignment(src, dst, with_scale=False):
    """
    src: Nx3
    dst: Nx3
    return: scale, R, t
    使得: dst ~= scale * R @ src + t
    """
    assert src.shape == dst.shape
    n = src.shape[0]
    dim = src.shape[1]

    mean_src = src.mean(axis=0)
    mean_dst = dst.mean(axis=0)

    src_demean = src - mean_src
    dst_demean = dst - mean_dst

    cov = (dst_demean.T @ src_demean) / n

    U, D, Vt = np.linalg.svd(cov)
    S = np.eye(dim)

    if np.linalg.det(U) * np.linalg.det(Vt) < 0:
        S[-1, -1] = -1

    R = U @ S @ Vt

    if with_scale:
        var_src = np.mean(np.sum(src_demean ** 2, axis=1))
        scale = np.trace(np.diag(D) @ S) / var_src
    else:
        scale = 1.0

    t = mean_dst - scale * (R @ mean_src)

    return scale, R, t


# =========================
# 将估计轨迹对齐到 gt
# =========================
def align_est_to_ref(ts_ref, xyz_ref, ts_est, xyz_est, max_diff=0.05):
    matched_ref, matched_est = associate_by_timestamp(
        ts_ref, xyz_ref, ts_est, xyz_est, max_diff=max_diff
    )

    if matched_ref is None or matched_est is None:
        print("[WARN] 匹配点过少，无法对齐，直接使用原始轨迹。")
        return xyz_est

    scale, R, t = umeyama_alignment(matched_est, matched_ref, with_scale=False)
    aligned = (scale * (R @ xyz_est.T)).T + t
    return aligned


# =========================
# 计算所有轨迹的显示范围
# =========================
def compute_xy_limits(*xyz_list, pad_ratio=0.05):
    all_xy = np.vstack([xyz[:, :2] for xyz in xyz_list if xyz is not None and len(xyz) > 0])
    xmin, ymin = all_xy.min(axis=0)
    xmax, ymax = all_xy.max(axis=0)

    dx = xmax - xmin
    dy = ymax - ymin

    pad_x = max(dx * pad_ratio, 0.2)
    pad_y = max(dy * pad_ratio, 0.2)

    return (xmin - pad_x, xmax + pad_x), (ymin - pad_y, ymax + pad_y)


# =========================
# 画轨迹
# =========================
def plot_traj(ax, gt_xyz, vins_xyz, dr_xyz, legend_loc):
    ax.plot(
        gt_xyz[:, 0], gt_xyz[:, 1],
        "--", color=GT_COLOR, linewidth=TRAJ_LW_GT, label="groundtruth"
    )
    ax.plot(
        vins_xyz[:, 0], vins_xyz[:, 1],
        "-", color=VINS_COLOR, linewidth=TRAJ_LW_EST, label="VINS-Mono"
    )
    ax.plot(
        dr_xyz[:, 0], dr_xyz[:, 1],
        "-", color=DR_COLOR, linewidth=TRAJ_LW_EST, label="DR-VINS"
    )

    ax.set_xlabel("x (m)", fontsize=LABEL_FS)
    ax.set_ylabel("y (m)", fontsize=LABEL_FS)
    ax.tick_params(labelsize=TICK_FS)
    ax.grid(True, alpha=0.35)
    ax.set_aspect("equal", adjustable="box")
    ax.legend(loc=legend_loc, fontsize=LEGEND_FS, framealpha=0.9)


def main():
    parser = argparse.ArgumentParser(description="Trajectory plot with right-side zoom inset")
    parser.add_argument("--gt", required=True, help="groundtruth TUM file")
    parser.add_argument("--vins", required=True, help="VINS trajectory TUM file")
    parser.add_argument("--dr", required=True, help="DR-VINS trajectory TUM file")
    parser.add_argument("--out", required=True, help="output image path")
    parser.add_argument("--title", default="", help="figure title")
    parser.add_argument("--max_diff", type=float, default=0.05, help="timestamp association max diff")
    parser.add_argument("--zoom_xlim", nargs=2, type=float, required=True, metavar=("XMIN", "XMAX"))
    parser.add_argument("--zoom_ylim", nargs=2, type=float, required=True, metavar=("YMIN", "YMAX"))
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 读入轨迹
    ts_gt, xyz_gt = load_tum(args.gt)
    ts_vins, xyz_vins = load_tum(args.vins)
    ts_dr, xyz_dr = load_tum(args.dr)

    # 对齐估计轨迹到 gt
    xyz_vins_aligned = align_est_to_ref(ts_gt, xyz_gt, ts_vins, xyz_vins, max_diff=args.max_diff)
    xyz_dr_aligned = align_est_to_ref(ts_gt, xyz_gt, ts_dr, xyz_dr, max_diff=args.max_diff)

    # 建图
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)

    # 左主图 / 右放大图
    ax_main = fig.add_axes([0.06, 0.12, 0.46, 0.78])
    ax_zoom = fig.add_axes([0.60, 0.24, 0.35, 0.54])

    # 主图绘制
    plot_traj(ax_main, xyz_gt, xyz_vins_aligned, xyz_dr_aligned, legend_loc="lower left")

    # 主图范围自动
    xlim_main, ylim_main = compute_xy_limits(xyz_gt, xyz_vins_aligned, xyz_dr_aligned, pad_ratio=0.05)
    ax_main.set_xlim(*xlim_main)
    ax_main.set_ylim(*ylim_main)

    # 标题
    if args.title.strip():
        fig.suptitle(args.title, fontsize=TITLE_FS, y=0.98)

    # 放大图绘制
    plot_traj(ax_zoom, xyz_gt, xyz_vins_aligned, xyz_dr_aligned, legend_loc="upper right")
    ax_zoom.set_xlim(args.zoom_xlim[0], args.zoom_xlim[1])
    ax_zoom.set_ylim(args.zoom_ylim[0], args.zoom_ylim[1])

    # 主图中的红框
    rect_x = args.zoom_xlim[0]
    rect_y = args.zoom_ylim[0]
    rect_w = args.zoom_xlim[1] - args.zoom_xlim[0]
    rect_h = args.zoom_ylim[1] - args.zoom_ylim[0]

    rect = Rectangle(
        (rect_x, rect_y), rect_w, rect_h,
        fill=False, edgecolor=BOX_COLOR, linewidth=BOX_LW
    )
    ax_main.add_patch(rect)

    # 蓝色直连线：从红框右上角 / 右下角 直接连接到右侧放大图左上角 / 左下角
    con_top = ConnectionPatch(
        xyA=(rect_x + rect_w, rect_y + rect_h), coordsA=ax_main.transData,
        xyB=(0.0, 1.0), coordsB=ax_zoom.transAxes,
        color=LINK_COLOR, linewidth=LINK_LW
    )
    con_bottom = ConnectionPatch(
        xyA=(rect_x + rect_w, rect_y), coordsA=ax_main.transData,
        xyB=(0.0, 0.0), coordsB=ax_zoom.transAxes,
        color=LINK_COLOR, linewidth=LINK_LW
    )
    fig.add_artist(con_top)
    fig.add_artist(con_bottom)

    # 统一边框稍微清晰一些
    for ax in [ax_main, ax_zoom]:
        for spine in ax.spines.values():
            spine.set_linewidth(1.1)

    plt.savefig(out_path, bbox_inches="tight")
    plt.close(fig)

    print(f"[OK] saved plot to: {out_path}")


if __name__ == "__main__":
    main()
