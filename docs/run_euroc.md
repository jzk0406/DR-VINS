# Dataset Preparation

Datasets are not included in this repository.

Expected dataset locations:

```bash
~/datasets
~/datasets/UMA-VI
~/datasets/vicon_room1
~/datasets/vicon_room2

```powershell
@'
# Run on EuRoC

This document provides notes for running DR-VINS on EuRoC sequences.

Typical command structure:

1. Start roscore.
2. Start the DR-VINS frontend node.
3. Start the loop fusion node.
4. Open RViz.
5. Play the EuRoC rosbag with `--clock`.

Detailed commands can be found in the main README.
