---
layout: blog
short_title: "Gymnasium/MuJoCo-v5 Environments"
subtitle: "New Features of Gymnasium/MuJoCo-v5 Environments and How to Load Third-Party Models"
title: "Releasing Gymnasium/MuJoCo-v5 Environments"
date: "2024-10-04"
excerpt: "We are excited to introduce version 5 of the MuJoCo Environments, bringing a wide variety of improvements, including the ability to load custom robot models."
Author: Kallinteris Andreas
thumbnail:
image:
read_time: 4
---

## Introduction
`Gymnasium/MuJoCo` is a set of robotics-based reinforcement learning environments using the [MuJoCo](https://mujoco.org/) physics engine, with various goals for the robot to learn, such as standing up, running quickly, or moving an arm to a point.

## A quick history of MuJoCo environments
The MuJoCo environments were originally introduced as version 0 in `gym==0.0.1` back in 2016, and were shortly followed by version 1 (`gym==0.1.0`) to address several configuration errors.
In 2018, version 2 was released in `gym==0.9.5`, bringing major backend improvements using the `mujoco-py>=1.5` simulator.
Version 3 (`gym==0.12.0` in 2018) offered increased customization options, enabling users to modify parts of the environment such as the reward function and slight adjustments to the robot model.
After Google DeepMind acquired MuJoCo, open-sourced the code and released a dedicated Python module (`mujoco`), version 4 ported the environments to the new `mujoco>=2.2.0` simulator, but removed the capability to slightly modify the environment.

The models in Gymnasium/MuJoCo were made around 2012; they pre-date the "modern" robotics revolution and are not realistic relative to actual robot systems.
All releases since version 1 provide useful additional customization options, back-end improvements and bug fixes, but use the same unrealistic robot models.

## MuJoCo v5
Over time, the MuJoCo environments have become standard testing environments in RL, used in hundreds if not thousands of academic papers at this point. They have provided a standard set of difficult-to-solve robotic environments, and have been a cornerstone in the development and evaluation of RL methods.

However, as RL methods continue to improve, the necessity for more complex robotic environments to evaluate them has become evident with state-of-the-art training algorithms, such as [TD3](https://arxiv.org/pdf/1802.09477.pdf) and [SAC](https://arxiv.org/pdf/1801.01290.pdf), being able to solve even the most complex of the MuJoCo problems.

We are pleased to announce version 5 of the Gymnasium/MuJoCo environments, released with `gymnasium==1.0.0`, with significantly increased customizability, bug fixes and overall faster step and reset speed.
```sh
pip install "gymnasium[mujoco]>=1.0.0"
```

```python
import gymnasium as gym

env = gym.make("Humanoid-v5")
```

## Key features
- Add support for loading third-party MuJoCo models, including realistic robot models, like those found in [MuJoCo Menagerie](https://github.com/deepmind/mujoco_menagerie).

- 80 enhancements, notably:
  - Performance: Improves training performance by removing a considerable amount of constant 0 observations from the observation spaces of the `Ant`, `Humanoid` and `HumanoidStandup` environments. This results in 5-7% faster training with `SB3/PPO` using `pytorch` (related [GitHub issue](https://github.com/Farama-Foundation/Gymnasium/issues/204)).
  - Customizability: Added new arguments for all the environments and restored the removed arguments from the `v3 → v4` transition.
  - Quality of life: Added new fields to `info` that include all reward components and non-observable state, and `reset()` now returns `info` which includes non-observable state elements.

- 24 bug fixes, notably:
  - Walker2D: Both feet now have `friction==1.9`, previously the right foot had `friction==0.9` and the left foot had `friction==1.9` (related [GitHub issue](https://github.com/Farama-Foundation/Gymnasium/issues/477)).
  - Pusher: The object (cylinder) was previously lighter than air, causing unexpected physics behaviour; its weight has been increased to a more realistic value (related [GitHub issue](https://github.com/Farama-Foundation/Gymnasium/issues/950)).
  - In Ant, Hopper, Humanoid, InvertedDoublePendulum, InvertedPendulum, Walker2d: `healthy_reward` was previously given on every step (even if the robot was unhealthy); now it is only given when the robot is healthy, resulting in faster learning. For further details about the performance impact of this change, see the related [GitHub issue](https://github.com/Farama-Foundation/Gymnasium/issues/526).
  - In Ant and Humanoid, the `contact_cost` reward component was previously always 0; it is now calculated correctly. For more information on the performance impact of this change, please check the related [GitHub issue #1](https://github.com/Farama-Foundation/Gymnasium/issues/504), [GitHub issue #2](https://github.com/Farama-Foundation/Gymnasium/issues/214).
  - In Reacher and Pusher, the reward function was calculated based on the previous state rather than the current state. For further information on the performance impact of this change, see the related [GitHub issue](https://github.com/Farama-Foundation/Gymnasium/issues/821).
  - Fixed several `info` fields.
    - Ant: Fixed `info["reward_ctrl"]` sometimes containing `contact_cost` instead of `ctrl_cost`.
    - Ant: Fixed `info["x_position"]`, `info["y_position"]` and `info["distance_from_origin"]` giving `xpos` instead of `qpos` observations (`xpos` observations are behind 1 `mj_step()`, for more details see [here](https://github.com/deepmind/mujoco/issues/889#issuecomment-1568896388)) (related [GitHub issue #1](https://github.com/Farama-Foundation/Gymnasium/issues/521) & [GitHub issue #2](https://github.com/Farama-Foundation/Gymnasium/issues/539)).
    - Pusher and Reacher: Fixed `info["reward_ctrl"]` not being multiplied by the reward weight.

- Generally improved documentation to explain the observation, action and reward functions in more detail.

## Example: using third-party MuJoCo robot models
For those looking for more complex real-world robot MuJoCo models, `v5` now supports custom robot models for each environment. Below, we show how this can be achieved using models from the [MuJoCo Menagerie](https://github.com/deepmind/mujoco_menagerie) project.

Depending on the robot type, we recommend using different environment models: for quadruped → `Ant-v5`, bipedal → `Humanoid-v5` and swimmer / crawler robots → `Swimmer-v5`.

However, it will be necessary to modify certain arguments in order to specify the desired behavior. The most commonly changed arguments are:
- `xml_file`: Path to the MuJoCo robot (MJCF or URDF file).
- `frame_skip`: The number of MuJoCo simulation steps per environment step, which sets the duration between steps, `dt = frame_skip * model.opt.timestep`. We recommend choosing `frame_skip` so that `dt` is in the range `[0.01, 0.1]`; smaller values allow more precise movements but require more actions to reach a goal.
- `ctrl_cost_weight`: The weight of control cost in the reward function, set it according to the needs of the robot. We recommend setting it to `0` at first for prototyping and increasing it as needed.
- `healthy_z_range`: The upper and lower limit the robot can be at without it being "unhealthy"; set it according to the height of the robot.

For more information on all the arguments, see the documentation pages of [`Ant`](https://gymnasium.farama.org/environments/mujoco/ant/), [`Humanoid`](https://gymnasium.farama.org/environments/mujoco/humanoid/) and [`Swimmer`](https://gymnasium.farama.org/environments/mujoco/swimmer/).

### Example [anybotics_anymal_b](https://github.com/deepmind/mujoco_menagerie/blob/main/anybotics_anymal_b/README.md)
```py
env = gym.make('Ant-v5', xml_file='./mujoco_menagerie/anybotics_anymal_b/scene.xml', ctrl_cost_weight=0.001, healthy_z_range=(0.48, 0.68), render_mode='human')
```

Here, we change the `xml_file` argument to load the new model, set the `healthy_z_range` because the robot has a different height than the default `Ant` robot, and reduce `ctrl_cost_weight`. In general, the `healthy_z_range` will need to be changed to fit each robot.

![](/assets/images/blogs/anymalb_small.gif)

### Example [Unitree Go1](https://github.com/deepmind/mujoco_menagerie/blob/main/unitree_go1/README.md)
```py
env = gym.make('Ant-v5', xml_file='./mujoco_menagerie/unitree_go1/scene.xml', healthy_z_range=(0.195, 0.75), ctrl_cost_weight=0.05)
```
The Go1 is a smaller quadruped, so the `healthy_z_range` is lowered to match its height, and the `ctrl_cost_weight` is increased to penalize large actions.

![](/assets/images/blogs/go1_small.gif)


### Example [Robotis OP3](https://github.com/deepmind/mujoco_menagerie/blob/main/robotis_op3/README.md)
```py
env = gym.make('Humanoid-v5', xml_file='./mujoco_menagerie/robotis_op3/scene.xml', healthy_z_range=(0.275, 0.5), include_cinert_in_observation=False, include_cvel_in_observation=False, include_qfrc_actuator_in_observation=False, include_cfrc_ext_in_observation=False, ctrl_cost_weight=0, contact_cost_weight=0)
```
For the OP3 humanoid, we disable the `cinert`, `cvel`, `qfrc_actuator` and `cfrc_ext` observations, as these are designed around the default `Humanoid` model and aren't needed for this robot. We also set the control and contact costs to `0` for prototyping.

![](/assets/images/blogs/robotisop3_small.gif)

For a more detailed tutorial, see [loading quadruped models](https://gymnasium.farama.org/main/tutorials/gymnasium_basics/load_quadruped_model/).

## Full Changelog
For more information about the development of the `Gymnasium/MuJoCo-v5` environments and a complete changelog, check the [GitHub PR](https://github.com/Farama-Foundation/Gymnasium/pull/572).
