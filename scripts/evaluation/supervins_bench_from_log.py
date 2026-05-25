#!/usr/bin/env python3
import re
import sys
from statistics import mean

if len(sys.argv) != 2:
    print("Usage: python3 supervins_bench_from_log.py /path/to/supervins.log")
    sys.exit(1)

log_path = sys.argv[1]

extract_times = []
match_times = []
feature_counts = []
match_counts = []

state = None

re_duration = re.compile(r"Duration:\s*([0-9.]+)\s*seconds")
re_features = re.compile(r"(\d+)\s+points extracted in current frame originally")
re_matches = re.compile(r"matches\.size\(\)\s*=\s*(\d+)")

with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if "extract feature time" in line:
            state = "extract"
            continue

        m = re_features.search(line)
        if m:
            feature_counts.append(int(m.group(1)))
            continue

        m = re_matches.search(line)
        if m:
            match_counts.append(int(m.group(1)))
            state = "match"
            continue

        m = re_duration.search(line)
        if m:
            t = float(m.group(1))
            if state == "extract":
                extract_times.append(t)
                state = None
            elif state == "match":
                match_times.append(t)
                state = None

def summarize(name, arr):
    if not arr:
        print(f"{name}: no data")
        return
    print(f"{name}: count={len(arr)}, mean={mean(arr):.6f}")

print("===== SuperVINS benchmark summary =====")

summarize("extract_times_sec", extract_times)
if extract_times:
    print(f"extract_fps = {1.0 / mean(extract_times):.3f}")

summarize("match_times_sec", match_times)
if match_times:
    print(f"match_fps = {1.0 / mean(match_times):.3f}")

summarize("feature_counts", feature_counts)
if feature_counts:
    print(f"avg_feature_points = {mean(feature_counts):.3f}")

summarize("match_counts", match_counts)
if match_counts:
    print(f"avg_matches = {mean(match_counts):.3f}")
    zero_match = sum(1 for x in match_counts if x == 0)
    print(f"zero_match_ratio = {zero_match}/{len(match_counts)} = {zero_match/len(match_counts):.3%}")
