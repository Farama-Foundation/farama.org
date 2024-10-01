---
layout: blog
short_title: "Gymnasium v1.0"
subtitle: "Gymansium v1.0: A Comprehensive Update, Summarising the Changes"
title: "Gymnasium v1.0: A Comprehensive Update"
date: "2024-10-01"
excerpt: ""
Author: Mark Towers and Jordan Terry
thumbnail:
image:
read_time: 5 minutes
---

**Gymnasium v1.0: A Comprehensive Update**

After years of hard work, Gymnasium v1.0 has officially arrived! This release marks a major milestone for the Gymnasium project, refining the core API, addressing bugs, and enhancing features. Over 200 pull requests have been merged since version 0.29.1, culminating in Gymnasium v1.0, a stable release focused on improving the API (`Env`, `Space`, and `VectorEnv`).

# v1.0 Summary
For a more detailed summary, see our [release notes](https://github.com/Farama-Foundation/Gymnasium/releases/tag/v1.0.0). We have also published a white paper on Gymnasium you can check out [here](https://arxiv.org/abs/2407.17032) and cite if using in academic work.

Let’s dive into some of the key changes!

## 1. **Removing the Plugin System**
One of the biggest changes in v1.0.0 is the removal of an undocumented plugin system that allowed for registering external environments behind the scenes. In previous versions, users could create environments like Atari or Minigrid without explicitly importing the relevant modules. Now, users will need to import these external libraries directly to register environments.

Example:
```python
import gymnasium as gym
import ale_py

gym.register_envs(ale_py)
env = gym.make("ALE/Pong-v5")
```
This change increases transparency and ensures a clearer workflow.

## 2. **Vector Environments Overhaul**
Vector environments have been significantly revamped. Previously, `VectorEnv` inherited from `Env`, which caused type-checking issues and made certain functionality harder to implement. In v1.0, `Env` and `VectorEnv` are now distinct, leading to clearer code and more efficient implementations.

Moreover, Gymnasium introduces the `gymnasium.make_vec` function for easier vectorized environment creation. The new setup allows users to specify vectorization modes like "sync" and "async," making it simpler to create and manage multiple environment instances simultaneously.

```python
envs = gym.make_vec("CartPole-v1", num_envs=3)
```

## 3. **Improved Wrappers**
With the separation of `Env` and `VectorEnv`, wrappers have also undergone changes. Wrappers that previously worked for both environments now have distinct variants for each. Standard environment wrappers are housed in `gymnasium.wrappers`, while vector-specific wrappers are found in `gymnasium.wrappers.vector`.

Several wrappers have been renamed or removed for clarity, such as: `AutoResetWrapper` -> `Autoreset` and `FrameStack` -> `FrameStackObservation`.
New wrappers have also been introduced, such as `DelayObservation` and `MaxAndSkipObservation`, to extend functionality.

### 4. **Functional Environments**
To enhance theoretical research and allow for easier integration into planning and search algorithms, Gymnasium introduces `FuncEnv`, a functional version of `Env`. This new environment type exposes functions such as `reward`, `observation`, and `transition`, allowing for more flexible control over the environment's behavior.

### 5. **Environment Version Changes**
Several popular environments have seen updates:
- **New MuJoCo v5** have been added to support the latest MuJoCo versions along with new features and bug fixes.
- **Lunar Lander** and **CarRacing** both received bug fixes, resulting in new environment versions.

## Moving ALE out of Gymnasium

Atari (Arcade Learning Environment / ALE) and Gymnasium (and Gym) have been interlinked over time with v1.0 finally separating the two as two fully separate project with a new ALE website. Given the Atari environments iconic history in reinforcement learning as the environments that Deep Reinforcement learning was first meaningfully demonstrated on and as some of the most iconic environments in Gymnasium, we wanted to give a bit of backstory on this decision.

The interface reinforcement learning researchers use for Atari environments is based on the Arcade Learning Environment (ALE), which was created at the University of Alberta as a C++ library in 2013 by some of the first researchers at DeepMind, including Marc Bellemare. A few years after this release, Python bindings were added to a public version of the ALE by Ben Goodrich, a researcher at the University of Tennessee (https://github.com/bbitmaster/ale_python_interface). This library was then forked by OpenAI, renamed Atari-Py, and released on PyPI as a dependency to enable Atari environments in Gymnasium.

This problem of having Gymnasium depend on a fork of a fork of the ALE meant that any changes (such as new environments) or bug fixes that occurred in the ALE were not available in Atari-Py, which included the benchmark for 56 Atari environments that DeepMind first used in their work showing human level performance in the environments. This was made worse by the fact that DeepMind had made their own major modifications and upgrades to the ALE in this time period (some were published publicly in [Xitari](https://github.com/google-deepmind/xitari), some were not). This created well founded scientific reproducibility concerns from the original ALE authors, which led to agreements between the original ALE authors and DeepMind and OpenAI to upstream python bindings from Atari-Py and to ALE and having Gym depend directly on the ALE, and for DeepMind to contribute all their code to the ALE so that the public could use it in a centralized and reproducible way. With the release of Gymnasium 1.0, we're finally completing this process of up streaming all Atari environments from the Gymnasium to the ALE.

To briefly elaborate on why we chose to fully move all the environments from Gymnasium to the ALE, it's because keeping the environments in Gymnasium left us with a few bad options:

1) Keep only the original Gym Atari environments in Gymnasium (which would mean ignoring environments included in the famous Atari 56 environments used by DeepMind)
2) Include all the ALE environments in Gymnasium (there's currently well over 100 and support for more games is being added regularly, and in general we try to be incredibly restrictive about environments being added to Gymnasium)
3) Move all Atari environments from Gymnasium to ale-py, separating the projects clearly with minimal overlap.

As a result, Atari documentation has been moved to [ale.farama.org](ale.farama.org) with the Gymnasium links redirecting users. We are maintaining `pip install "gymnasium[atari]"` (though removing `accept-rom-license` as this is unnecessary now) for backward compatibility. Most importantly, the plugin system described at the start of the blog will mean that users need to `import ale_py` in order to register environments.

# Looking Ahead
Gymnasium v1.0 brings a refined, clearer, and more efficient framework for creating and interacting with reinforcement learning environments. With a focus on long-term stability, we hope this release sets the foundation for future growth in the reinforcement learning community.
