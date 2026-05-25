\# DR-VINS: Robust Visual-Inertial SLAM for Degraded Scenes



DR-VINS is a visual-inertial SLAM experimental system designed for degraded visual environments such as low-texture scenes, illumination changes, over-exposure, and indoor-outdoor transitions. The project is based on the VINS-style visual-inertial estimation framework and introduces a deep feature matching frontend to improve localization robustness in challenging scenarios.



本项目为本科毕业设计实验系统，主要面向低纹理、光照变化、强光过曝和室内外切换等退化场景下的视觉惯性定位与建图问题。



\---



\## 1. Project Overview



Traditional visual-inertial SLAM methods may suffer from tracking instability or trajectory drift when visual features become sparse or unreliable. DR-VINS integrates a deep feature extraction and matching frontend with a VINS-style backend and loop fusion module, aiming to improve robustness under degraded visual conditions.



The project includes:



\- Modified SuperVINS / DR-VINS source code

\- EuRoC and UMA-VI configuration files

\- Evaluation and plotting scripts

\- Representative trajectory comparison results

\- Runtime analysis scripts

\- Demo screenshots and video links



\---



\## 2. Main Features



\- Visual-inertial odometry based on a VINS-style sliding window backend

\- Deep feature frontend using learned feature extraction and matching

\- Loop fusion and pose graph optimization

\- Support for EuRoC MAV dataset experiments

\- Support for UMA-VI degraded-scene dataset experiments

\- ATE evaluation using evo

\- Trajectory visualization and local zoom-in plotting scripts

\- Preliminary runtime analysis for frontend feature extraction and matching



\---



\## 3. Repository Structure



```text

DR-VINS/

├── src/

│   └── SuperVINS/                  # Main DR-VINS / SuperVINS source code

├── configs/

│   ├── euroc/                      # EuRoC-related configuration files

│   └── umavi/                      # UMA-VI-related configuration files

├── scripts/

│   ├── plotting/                   # Trajectory plotting scripts

│   ├── evaluation/                 # Runtime and ATE-related scripts

│   └── dataset\_tools/              # Dataset conversion tools

├── results/

│   ├── trajectory\_figures/         # Representative trajectory figures

│   ├── tables/                     # Final evaluation tables

│   └── runtime/                    # Runtime statistics

├── media/

│   ├── screenshots/                # RViz screenshots

│   └── demo\_links.md               # Demo video links

├── docs/

│   ├── environment.md              # Environment setup

│   ├── dataset\_preparation.md      # Dataset preparation

│   ├── run\_euroc.md                # EuRoC running instructions

│   ├── run\_umavi.md                # UMA-VI running instructions

│   ├── evaluation.md               # Evaluation instructions

│   └── known\_issues.md             # Notes and known issues

└── README.md

```



\---



\## 4. Environment



The experiments were conducted under the following environment:



\- Ubuntu 20.04 under WSL2

\- ROS Noetic

\- CMake / Catkin

\- OpenCV

\- Ceres Solver

\- Eigen

\- PyTorch / ONNX runtime dependencies for the deep frontend

\- evo for trajectory evaluation



A typical workspace structure is:



```bash

\~/catkin\_ws/src/SuperVINS

\~/ws\_vinsfusion/src/VINS-Fusion

\~/datasets

\~/results

```



Please refer to `docs/environment.md` for detailed setup instructions.



\---



\## 5. Dataset Preparation



This project uses the following datasets.



\### EuRoC MAV Dataset



Representative sequences include:



\- MH\_01\_easy

\- MH\_05\_difficult

\- V1\_03\_difficult

\- V2\_02\_medium

\- V2\_03\_difficult



Example directory structure:



```bash

\~/datasets/vicon\_room2/V2\_03\_difficult/V2\_03\_difficult.bag

```



\### UMA-VI Dataset



Representative degraded sequences include:



\- corridor-eng\_LowText

\- parking-csc1\_LowText

\- conference-csc2\_IllChange

\- third-floor-csc1\_IllChange

\- two-floors-csc1\_InOut

\- fantasy-csc1\_SunOver

\- parking-eng1\_SunOver

\- lab-module-csc\_InOut



Example directory structure:



```bash

\~/datasets/UMA-VI/corridor-eng\_LowText/corridor\_cam2\_imu0.bag

```



Datasets are not included in this repository due to their large file size.



\---



\## 6. Running Examples



\### 6.1 Run DR-VINS on a UMA-VI Sequence



Example: `corridor-eng\_LowText`



Terminal 1:



```bash

source /opt/ros/noetic/setup.bash

source \~/catkin\_ws/devel/setup.bash



roscore

```



Terminal 2:



```bash

source /opt/ros/noetic/setup.bash

source \~/catkin\_ws/devel/setup.bash



rosparam set use\_sim\_time true



rosrun supervins supervins\_node \\

&#x20; \~/catkin\_ws/src/SuperVINS/config/euroc/umavi\_corridor\_hybrid\_frontend.yaml

```



Terminal 3:



```bash

source /opt/ros/noetic/setup.bash

source \~/catkin\_ws/devel/setup.bash



rosparam set use\_sim\_time true



rosrun hybrid\_loop\_fusion hybrid\_loop\_fusion\_node \\

&#x20; \~/catkin\_ws/src/SuperVINS/config/euroc/umavi\_corridor\_hybrid\_loop.yaml

```



Terminal 4:



```bash

source /opt/ros/noetic/setup.bash

source \~/catkin\_ws/devel/setup.bash



rviz -d \~/catkin\_ws/src/SuperVINS/config/supervins\_rviz\_config.rviz

```



Terminal 5:



```bash

source /opt/ros/noetic/setup.bash

source \~/catkin\_ws/devel/setup.bash



rosbag play --clock --pause -r 1.0 \\

&#x20; \~/datasets/UMA-VI/corridor-eng\_LowText/corridor\_cam2\_imu0.bag

```



\---



\## 7. Evaluation



Absolute Trajectory Error is evaluated using `evo\_ape`.



Example:



```bash

evo\_ape tum \\

&#x20; gt.tum \\

&#x20; estimated.tum \\

&#x20; -va --align --t\_max\_diff 0.05

```



Trajectory visualization:



```bash

evo\_traj tum \\

&#x20; VINS-Fusion.tum \\

&#x20; DR-VINS.tum \\

&#x20; --ref gt.tum \\

&#x20; --align \\

&#x20; --t\_max\_diff 0.05 \\

&#x20; --plot \\

&#x20; --plot\_mode xy

```



For local zoom-in trajectory figures, use:



```bash

python3 scripts/plotting/plot\_traj\_with\_inset.py \\

&#x20; --gt gt.tum \\

&#x20; --vins VINS-Fusion.tum \\

&#x20; --dr DR-VINS.tum \\

&#x20; --out output.png \\

&#x20; --title "" \\

&#x20; --max\_diff 0.05 \\

&#x20; --zoom\_xlim xmin xmax \\

&#x20; --zoom\_ylim ymin ymax

```



\---



\## 8. Representative Results



The experiments show that DR-VINS improves trajectory stability in several degraded scenes, especially under low-texture, illumination-change, and indoor-outdoor transition conditions.



Representative visual results are provided in:



```text

results/trajectory\_figures/

media/screenshots/

```



Demo videos are listed in:



```text

media/demo\_links.md

```



\---



\## 9. Runtime Notes



A preliminary runtime analysis was conducted on the EuRoC `MH\_01\_easy` sequence. The observed frontend statistics were:



| Metric | Result |

|---|---:|

| Average feature extraction time | 0.013860 s |

| Feature extraction FPS | 72.148 FPS |

| Average feature matching time | 0.028893 s |

| Feature matching FPS | 34.610 FPS |

| Average number of feature points | 1107.411 |

| Average number of matches | 687.287 |

| Pose output frequency | approximately 10 Hz |



These results indicate that the frontend has quasi-real-time processing capability under the tested environment. However, strict real-time performance across different hardware platforms and all dataset sequences requires further systematic evaluation.



\---



\## 10. Notes and Known Issues



\- The system was mainly evaluated using offline rosbag playback.

\- Some sequences are sensitive to initialization, ROS node states, output paths, and runtime load.

\- For stable experiments, it is recommended to:

&#x20; - restart `roscore` before each run;

&#x20; - clean old ROS nodes;

&#x20; - use independent absolute output paths;

&#x20; - avoid mixing old pose graph outputs;

&#x20; - run numerical evaluation separately from heavy RViz recording.

\- RViz loop visualization and loop optimization output are not always equivalent. Loop effectiveness should be judged using trajectory files and ATE results.



\---



\## 11. Acknowledgements



This project is based on and inspired by the following open-source projects:



\- VINS-Fusion

\- SuperVINS

\- evo trajectory evaluation toolbox



The baseline VINS-Fusion system is used for comparative experiments. Please refer to the original repositories for their official implementations and licenses.



\---



\## 12. License



This repository is released for academic and research purposes. Please check the licenses of the upstream projects before redistribution or commercial use.

