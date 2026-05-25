# Evaluation

Trajectory evaluation is performed using evo.

Example:

```bash
evo_ape tum gt.tum estimated.tum -va --align --t_max_diff 0.05
evo_traj tum estimated.tum --ref gt.tum --align --t_max_diff 0.05 --plot --plot_mode xy

```powershell
@'
# Known Issues

- Some sequences are sensitive to initialization and ROS node states.
- It is recommended to restart `roscore` before each independent run.
- Old pose graph outputs should not be mixed with new experiments.
- Heavy RViz visualization may affect runtime performance.
- Loop visualization in RViz is not always equivalent to loop optimization effectiveness.
