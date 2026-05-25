# \# DR-VINS：面向退化场景的鲁棒视觉惯性 SLAM 系统

# 

# \[English](README.md) | \[中文](README\_zh-CN.md)

# 

# DR-VINS 是一个面向退化视觉场景的视觉惯性 SLAM 实验系统。项目基于 VINS 系列视觉惯性估计框架，引入深度特征提取与匹配前端，用于提升系统在低纹理、光照变化、强光过曝和室内外切换等困难场景下的定位稳定性和鲁棒性。

# 

# 本项目为本科毕业设计实验系统，主要用于验证多传感器融合定位与建图方法在标准视觉惯性数据集和退化视觉场景数据集上的表现。

# 

# \---

# 

# \## 目录

# 

# \- \[1. 项目简介](#1-项目简介)

# \- \[2. 主要功能](#2-主要功能)

# \- \[3. 仓库结构](#3-仓库结构)

# \- \[4. 实验环境](#4-实验环境)

# \- \[5. 数据集准备](#5-数据集准备)

# \- \[6. 运行方法](#6-运行方法)

# \- \[7. 结果评估](#7-结果评估)

# \- \[8. 实验结果展示](#8-实验结果展示)

# \- \[9. 运行视频](#9-运行视频)

# \- \[10. 实时性说明](#10-实时性说明)

# \- \[11. 注意事项](#11-注意事项)

# \- \[12. 致谢](#12-致谢)

# \- \[13. License](#13-license)

# 

# \---

# 

# \## 1. 项目简介

# 

# 传统视觉惯性 SLAM 方法在低纹理、光照变化、强光过曝以及室内外切换等场景下，容易出现特征跟踪不稳定、匹配点数量不足、轨迹漂移甚至定位失败等问题。为提高系统在退化视觉环境下的鲁棒性，本文在 VINS 风格的视觉惯性估计框架基础上，引入深度特征提取与匹配前端，并结合回环检测与位姿图优化模块，构建了 DR-VINS 实验系统。

# 

# 本仓库主要包含以下内容：

# 

# \- 修改后的 SuperVINS / DR-VINS 源码；

# \- EuRoC 与 UMA-VI 数据集相关配置文件；

# \- 轨迹评估、绘图和数据处理脚本；

# \- 代表性轨迹对比图；

# \- 前端运行时间统计脚本；

# \- RViz 运行视频链接。

# 

# \---

# 

# \## 2. 主要功能

# 

# \- 基于 VINS 风格滑动窗口后端的视觉惯性里程计；

# \- 引入深度特征提取与匹配前端，提高困难场景中的特征关联能力；

# \- 支持回环检测与位姿图优化；

# \- 支持 EuRoC MAV 数据集实验；

# \- 支持 UMA-VI 退化视觉场景数据集实验；

# \- 支持使用 evo 进行 ATE 轨迹精度评估；

# \- 提供轨迹对比图和局部放大图绘制脚本；

# \- 提供前端特征提取和匹配耗时统计脚本。

# 

# \---

# 

# \## 3. 仓库结构

# 

# ```text

# DR-VINS/

# ├── src/

# │   └── SuperVINS/                  # DR-VINS / SuperVINS 主体源码

# ├── configs/

# │   ├── euroc/                      # EuRoC 相关配置文件

# │   └── umavi/                      # UMA-VI 相关配置文件

# ├── scripts/

# │   ├── plotting/                   # 轨迹绘图脚本

# │   ├── evaluation/                 # 运行时间与评估相关脚本

# │   └── dataset\_tools/              # 数据集转换工具

# ├── results/

# │   └── trajectory\_figures/         # 代表性轨迹对比图

# ├── media/

# │   ├── screenshots/                # RViz 截图

# │   └── demo\_links.md               # 运行视频链接

# ├── docs/

# │   ├── environment.md              # 环境配置说明

# │   ├── dataset\_preparation.md      # 数据集准备说明

# │   ├── run\_euroc.md                # EuRoC 运行说明

# │   ├── run\_umavi.md                # UMA-VI 运行说明

# │   ├── evaluation.md               # 评估说明

# │   └── known\_issues.md             # 已知问题说明

# └── README.md

# ```

# 

# \---

# 

# \## 4. 实验环境

# 

# 本项目主要在以下环境下完成实验：

# 

# \- Ubuntu 20.04 under WSL2

# \- ROS Noetic

# \- CMake / Catkin

# \- OpenCV

# \- Ceres Solver

# \- Eigen

# \- PyTorch / ONNX Runtime 相关依赖

# \- evo 轨迹评估工具

# 

# 典型工作区结构如下：

# 

# ```bash

# \~/catkin\_ws/src/SuperVINS

# \~/ws\_vinsfusion/src/VINS-Fusion

# \~/datasets

# \~/results

# ```

# 

# 更详细的环境配置说明见 \[`docs/environment.md`](docs/environment.md)。

# 

# \---

# 

# \## 5. 数据集准备

# 

# 本项目主要使用 EuRoC MAV 数据集和 UMA-VI 数据集。由于数据集体积较大，仓库中不包含原始 rosbag 数据。

# 

# \### 5.1 EuRoC MAV 数据集

# 

# 代表性测试序列包括：

# 

# \- `MH\_01\_easy`

# \- `MH\_05\_difficult`

# \- `V1\_03\_difficult`

# \- `V2\_02\_medium`

# \- `V2\_03\_difficult`

# 

# 示例目录结构：

# 

# ```bash

# \~/datasets/vicon\_room2/V2\_03\_difficult/V2\_03\_difficult.bag

# ```

# 

# \### 5.2 UMA-VI 数据集

# 

# 代表性退化场景序列包括：

# 

# \- `corridor-eng\_LowText`

# \- `parking-csc1\_LowText`

# \- `conference-csc2\_IllChange`

# \- `third-floor-csc1\_IllChange`

# \- `two-floors-csc1\_InOut`

# \- `fantasy-csc1\_SunOver`

# \- `parking-eng1\_SunOver`

# \- `lab-module-csc\_InOut`

# 

# 示例目录结构：

# 

# ```bash

# \~/datasets/UMA-VI/corridor-eng\_LowText/corridor\_cam2\_imu0.bag

# ```

# 

# \---

# 

# \## 6. 运行方法

# 

# 下面以 UMA-VI 数据集中的 `corridor-eng\_LowText` 序列为例，说明 DR-VINS Loop 的运行方式。

# 

# \### 终端 1：启动 roscore

# 

# ```bash

# source /opt/ros/noetic/setup.bash

# source \~/catkin\_ws/devel/setup.bash

# 

# roscore

# ```

# 

# \### 终端 2：启动 DR-VINS 前端

# 

# ```bash

# source /opt/ros/noetic/setup.bash

# source \~/catkin\_ws/devel/setup.bash

# 

# rosparam set use\_sim\_time true

# 

# rosrun supervins supervins\_node \\

# &#x20; \~/catkin\_ws/src/SuperVINS/config/euroc/umavi\_corridor\_hybrid\_frontend.yaml

# ```

# 

# \### 终端 3：启动回环模块

# 

# ```bash

# source /opt/ros/noetic/setup.bash

# source \~/catkin\_ws/devel/setup.bash

# 

# rosparam set use\_sim\_time true

# 

# rosrun hybrid\_loop\_fusion hybrid\_loop\_fusion\_node \\

# &#x20; \~/catkin\_ws/src/SuperVINS/config/euroc/umavi\_corridor\_hybrid\_loop.yaml

# ```

# 

# \### 终端 4：打开 RViz

# 

# ```bash

# source /opt/ros/noetic/setup.bash

# source \~/catkin\_ws/devel/setup.bash

# 

# rviz -d \~/catkin\_ws/src/SuperVINS/config/supervins\_rviz\_config.rviz

# ```

# 

# \### 终端 5：播放 rosbag

# 

# ```bash

# source /opt/ros/noetic/setup.bash

# source \~/catkin\_ws/devel/setup.bash

# 

# rosbag play --clock --pause -r 1.0 \\

# &#x20; \~/datasets/UMA-VI/corridor-eng\_LowText/corridor\_cam2\_imu0.bag

# ```

# 

# 建议在所有节点和 RViz 启动完成后，再按空格开始播放 rosbag。

# 

# \---

# 

# \## 7. 结果评估

# 

# 本项目使用 `evo\_ape` 计算绝对轨迹误差 ATE。

# 

# ```bash

# evo\_ape tum \\

# &#x20; gt.tum \\

# &#x20; estimated.tum \\

# &#x20; -va --align --t\_max\_diff 0.05

# ```

# 

# 轨迹可视化可以使用 `evo\_traj`：

# 

# ```bash

# evo\_traj tum \\

# &#x20; VINS-Fusion.tum \\

# &#x20; DR-VINS.tum \\

# &#x20; --ref gt.tum \\

# &#x20; --align \\

# &#x20; --t\_max\_diff 0.05 \\

# &#x20; --plot \\

# &#x20; --plot\_mode xy

# ```

# 

# 如需绘制带局部放大区域的轨迹对比图，可以使用：

# 

# ```bash

# python3 scripts/plotting/plot\_traj\_with\_inset.py \\

# &#x20; --gt gt.tum \\

# &#x20; --vins VINS-Fusion.tum \\

# &#x20; --dr DR-VINS.tum \\

# &#x20; --out output.png \\

# &#x20; --title "" \\

# &#x20; --max\_diff 0.05 \\

# &#x20; --zoom\_xlim xmin xmax \\

# &#x20; --zoom\_ylim ymin ymax

# ```

# 

# \---

# 

# \## 8. 实验结果展示

# 

# 本节展示 DR-VINS 在 EuRoC 和 UMA-VI 数据集上的代表性实验结果，包括轨迹对比图、退化场景表现和部分定量结果。

# 

# \### 8.1 EuRoC 轨迹对比

# 

# \#### EuRoC MH01

# 

# !\[MH01 trajectory comparison](results/trajectory\_figures/MH01\_inset\_right\_VINS\_vs\_DR-VINS.png)

# 

# \#### EuRoC MH05

# 

# !\[MH05 trajectory comparison](results/trajectory\_figures/MH05\_inset\_right\_VINS\_vs\_DR-VINS.png)

# 

# \#### EuRoC V1\_03

# 

# !\[V1\_03 trajectory comparison](results/trajectory\_figures/V1\_03\_inset\_right\_VINS\_vs\_DR-VINS.png)

# 

# \### 8.2 UMA-VI 退化场景轨迹对比

# 

# \#### UMA-VI corridor-eng\_LowText

# 

# !\[corridor-eng\_LowText trajectory comparison](results/trajectory\_figures/corridor-eng\_LowText\_VINS-Fusion\_vs\_DR-VINS\_trajectories.png)

# 

# \#### UMA-VI parking-csc1\_LowText

# 

# !\[parking-csc1\_LowText trajectory comparison](results/trajectory\_figures/parking-csc1\_LowText\_VINS-Fusion\_vs\_DR-VINS\_trajectories.png)

# 

# \#### UMA-VI conference-csc2\_IllChange

# 

# !\[conference-csc2\_IllChange trajectory comparison](results/trajectory\_figures/conference-csc2\_IllChange\_relaxed\_clean\_fixed\_legend\_trajectories.png)

# 

# \### 8.3 定量结果

# 

# 部分代表性序列的 ATE RMSE 结果如下：

# 

# | Dataset | Sequence | VINS-Fusion | VINS-Fusion Loop | DR-VINS | DR-VINS Loop |

# |---|---|---:|---:|---:|---:|

# | EuRoC | V2\_02\_medium | 0.144 | 0.106 | 0.092 | 0.059 |

# | EuRoC | V2\_03\_difficult | 0.205 | 0.097 | 0.191 | 0.139 |

# | UMA-VI | corridor-eng\_LowText | 0.409 | 0.382 | 0.690 | 0.059 |

# | UMA-VI | conference-csc2\_IllChange | 0.798 | 0.803 | 0.038 | 0.019 |

# | UMA-VI | third-floor-csc1\_IllChange | failed | failed | 0.063 | 0.042 |

# | UMA-VI | two-floors-csc1\_InOut | failed | failed | 1.513 | 0.088 |

# 

# 更多轨迹图见 \[`results/trajectory\_figures`](results/trajectory\_figures)。

# 

# \---

# 

# \## 9. 运行视频

# 

# 代表性 RViz 运行视频已上传至 GitHub Releases：

# 

# \- \[DR-VINS Demo Videos Release](https://github.com/jzk0406/DR-VINS/releases/tag/v1.0-demo)

# \- \[运行视频列表](media/demo\_links.md)

# 

# 视频内容包括 EuRoC 和 UMA-VI 序列的 RViz 运行画面，展示了轨迹输出、特征跟踪、点云可视化和回环相关结果。

# 

# \---

# 

# \## 10. 实时性说明

# 

# 本文对 DR-VINS 前端运行耗时进行了初步统计。以 EuRoC `MH\_01\_easy` 序列为例，前端运行统计结果如下：

# 

# | 指标 | 结果 |

# |---|---:|

# | 特征提取平均耗时 | 0.013860 s |

# | 特征提取帧率 | 72.148 FPS |

# | 特征匹配平均耗时 | 0.028893 s |

# | 特征匹配帧率 | 34.610 FPS |

# | 平均特征点数量 | 1107.411 |

# | 平均匹配数量 | 687.287 |

# | 位姿输出频率 | 约 10 Hz |

# 

# 上述结果说明，在当前实验平台和测试序列下，DR-VINS 前端具备一定的准实时处理能力。但由于尚未在不同硬件平台和所有数据集序列下进行统一统计，因此严格实时性仍需后续进一步验证。

# 

# \---

# 

# \## 11. 注意事项

# 

# \- 本项目主要基于离线 rosbag 回放进行实验。

# \- 部分序列对初始化状态、ROS 节点状态、输出路径和运行负载较敏感。

# \- 建议每次独立运行前重启 `roscore`。

# \- 建议清理旧的 ROS 节点和历史输出文件。

# \- 建议使用独立的绝对输出路径，避免混用旧的 pose graph 结果。

# \- 建议将数值评估和高负载 RViz 录屏分开进行。

# \- RViz 中的回环可视化不完全等价于回环优化是否生效，回环效果应主要依据轨迹文件和 ATE 结果判断。

# 

# \---

# 

# \## 12. 致谢

# 

# 本项目参考和使用了以下开源项目：

# 

# \- VINS-Fusion

# \- SuperVINS

# \- evo trajectory evaluation toolbox

# 

# 其中，VINS-Fusion 作为基线方法用于对比实验。相关源码和许可证请参考原项目仓库。

# 

# \---

# 

# \## 13. License

# 

# This repository is released for academic and research purposes. Please check the licenses of the upstream projects before redistribution or commercial use.

