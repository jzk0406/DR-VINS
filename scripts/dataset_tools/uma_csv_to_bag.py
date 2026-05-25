#!/usr/bin/env python3
import csv
import argparse
from pathlib import Path

import cv2
import rosbag
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, Imu


def ns_to_ros_time(ns: int) -> rospy.Time:
    secs = ns // 1_000_000_000
    nsecs = ns % 1_000_000_000
    return rospy.Time(secs, nsecs)


def load_cam_csv(cam_csv_path: Path):
    rows = []
    with cam_csv_path.open("r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            # timestamp [ns], filename, exposure [ns]
            ts = int(row[0])
            filename = row[1]
            rows.append((ts, filename))
    return rows


def load_imu_csv(imu_csv_path: Path):
    rows = []
    with imu_csv_path.open("r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            # timestamp [ns], wx, wy, wz, ax, ay, az
            ts = int(row[0])
            wx, wy, wz = map(float, row[1:4])
            ax, ay, az = map(float, row[4:7])
            rows.append((ts, wx, wy, wz, ax, ay, az))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seq_dir", required=True, help="UMA-VI sequence directory")
    parser.add_argument("--cam", default="cam2", help="camera folder name, e.g. cam2")
    parser.add_argument("--bag_out", required=True, help="output bag path")
    parser.add_argument("--image_topic", default="/cam0/image_raw")
    parser.add_argument("--imu_topic", default="/imu0")
    args = parser.parse_args()

    seq_dir = Path(args.seq_dir).expanduser().resolve()
    cam_dir = seq_dir / args.cam
    cam_csv = cam_dir / "data.csv"
    img_dir = cam_dir / "data"
    imu_csv = seq_dir / "imu0" / "data.csv"
    bag_out = Path(args.bag_out).expanduser().resolve()

    if not cam_csv.exists():
        raise FileNotFoundError(f"camera csv not found: {cam_csv}")
    if not img_dir.exists():
        raise FileNotFoundError(f"image dir not found: {img_dir}")
    if not imu_csv.exists():
        raise FileNotFoundError(f"imu csv not found: {imu_csv}")

    cam_rows = load_cam_csv(cam_csv)
    imu_rows = load_imu_csv(imu_csv)

    print(f"Loaded {len(cam_rows)} image rows from {cam_csv}")
    print(f"Loaded {len(imu_rows)} imu rows from {imu_csv}")
    print(f"Writing bag to: {bag_out}")

    bag_out.parent.mkdir(parents=True, exist_ok=True)
    bridge = CvBridge()

    i = 0
    j = 0
    with rosbag.Bag(str(bag_out), "w") as bag:
        while i < len(cam_rows) or j < len(imu_rows):
            use_cam = False
            if i < len(cam_rows) and j < len(imu_rows):
                use_cam = cam_rows[i][0] <= imu_rows[j][0]
            elif i < len(cam_rows):
                use_cam = True

            if use_cam:
                ts_ns, filename = cam_rows[i]
                img_path = img_dir / filename
                img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
                if img is None:
                    raise RuntimeError(f"failed to read image: {img_path}")

                msg: Image = bridge.cv2_to_imgmsg(img, encoding="mono8")
                msg.header.stamp = ns_to_ros_time(ts_ns)
                msg.header.frame_id = args.cam
                bag.write(args.image_topic, msg, msg.header.stamp)
                i += 1
            else:
                ts_ns, wx, wy, wz, ax, ay, az = imu_rows[j]
                msg = Imu()
                msg.header.stamp = ns_to_ros_time(ts_ns)
                msg.header.frame_id = "imu0"

                msg.orientation_covariance[0] = -1.0  # orientation unavailable
                msg.angular_velocity.x = wx
                msg.angular_velocity.y = wy
                msg.angular_velocity.z = wz
                msg.linear_acceleration.x = ax
                msg.linear_acceleration.y = ay
                msg.linear_acceleration.z = az

                bag.write(args.imu_topic, msg, msg.header.stamp)
                j += 1

    print("Done.")


if __name__ == "__main__":
    main()
