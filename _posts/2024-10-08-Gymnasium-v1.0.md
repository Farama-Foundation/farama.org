---
layout: blog
short_title: "Gymnasium v1.0"
subtitle: "Gymansium v1.0: A Comprehensive Update, Summarising the Changes"
title: "Gymnasium v1.0: A Comprehensive Update"
date: "2024-10-08"
excerpt: "After years of hard work, Gymnasium v1.0 has officially arrived! This release marks a major milestone for the Gymnasium project, refining the core API, addressing bugs, and enhancing features. Over 200 pull requests have been merged since version 0.29.1, culminating in Gymnasium v1.0, a stable release focused on improving the API (`Env`, `Space`, and `VectorEnv`). This post summarizes these changes."
Author: Mark Towers, Jordan Terry, and Ariel Kwiatkowski
thumbnail:
image:
read_time: 5
---

# Gymnasium v1.0: A Comprehensive Update**

After years of hard work, Gymnasium v1.0 has officially arrived! This release marks a major milestone for the Gymnasium project, refining the core API, addressing bugs, and enhancing features. Over 200 pull requests have been merged since version 0.29.1, culminating in Gymnasium v1.0, a stable release focused on improving the API (`Env`, `Space`, and `VectorEnv`).

For a more detailed summary, see our [release notes](https://github.com/Farama-Foundation/Gymnasium/releases/tag/v1.0.0). We have also published a white paper on Gymnasium you can check out [here](https://arxiv.org/abs/2407.17032) and cite if using in academic work.

Let’s dive into some of the key changes!

## 1. **Vector Environments Overhaul**
Vector environments have been significantly revamped. Previously, `VectorEnv` inherited from `Env`, which wasn't technically valid, and caused various issues with method signatures. In v1.0, `Env` and `VectorEnv` are now distinct and fully supported, leading to clearer code and more efficient implementations.

Moreover, Gymnasium introduces the `gymnasium.make_vec` function for easier vectorized environment creation. The new setup allows users to specify a vectorization mode (by default: "sync", "async" or "vector_entry_point") making it simpler to create and manage multiple environment instances simultaneously.

```python
envs = gym.make_vec("CartPole-v1", num_envs=3, vectorization_mode="vector_entry_point")
```

With this, we also support custom vectorization, defined for each environment separately, which allows for significantly more efficient implementations in certain cases.

We also changed the auto-reset behavior of vectorized environments. In the past, when an episode terminated (or was truncated), it would immediately reset, with the final observation being passed in the `info` dict. This was less than ideal, as `info` was primarily intended for auxiliary information, not the main observations. Now, the observation returned alongside `terminated | truncated == True` is the final observation of the episode that just finished. The action following that will be ignored and treated as a reset signal, after which the new episode will begin. We will further elaborate on this in a future blog post.

## 2. **Improved Wrappers**
With the separation of `Env` and `VectorEnv`, wrappers have also undergone changes. Wrappers that previously worked for both environments now have distinct variants for each. Standard environment wrappers are housed in `gymnasium.wrappers`, while vector-specific wrappers are found in `gymnasium.wrappers.vector`.

Several wrappers have been renamed or removed for clarity, such as: `AutoResetWrapper` -> `Autoreset` and `FrameStack` -> `FrameStackObservation`.
New wrappers have also been introduced, such as `DelayObservation` and `MaxAndSkipObservation`, to extend functionality.

### 3. **Functional Environments**
To enable a different coding paradigm and allow for easier integration into planning algorithms, Gymnasium introduces `FuncEnv`, a functional version of `Env`. This new environment type exposes functions such as `reward`, `observation`, and `transition`, allowing for more flexible control over the environment's behavior. Furthermore, functional environments implemented in JAX can often be jitted and vmapped, leading to massive performance improvements and easy hardware acceleration.

### 4. **Environment Version Changes**
Several popular environments have seen updates:
- **New MuJoCo v5** have been added to support the latest MuJoCo versions along with new features and bug fixes.
- **Lunar Lander** and **CarRacing** both received bug fixes, resulting in new environment versions.

## 5. **Removing the Plugin System**
In version 1.0 we removed an undocumented plugin system that allowed for registering external environments behind the scenes. In previous versions, users could create environments like Atari or Minigrid without explicitly importing the relevant modules. Now, users will need to import these external libraries directly to register environments.

Example:
```python
import gymnasium as gym
import ale_py

gym.register_envs(ale_py)  # optional
env = gym.make("ALE/Pong-v5")
```
This change increases security, transparency and ensures a clearer workflow.

## Moving ALE out of Gymnasium

Atari (Arcade Learning Environment / ALE) and Gymnasium (and Gym) have been interlinked over the course of their existence. With v1.0 we decided to properly split them into two separate projects, with a new dedicated [ALE website](https://ale.farama.org). Given the Atari environments' iconic history in reinforcement learning, we wanted to give a bit of backstory on this decision.

The interface reinforcement learning researchers use for Atari environments is based on the Arcade Learning Environment (ALE), which was created at the University of Alberta as a C++ library in 2013 by some of the first researchers at DeepMind, including Marc Bellemare. A few years after this release, Python bindings were added to a public version of the ALE by Ben Goodrich, a researcher at the University of Tennessee (https://github.com/bbitmaster/ale_python_interface). This library was then forked by OpenAI, renamed Atari-Py, and released on PyPI as a dependency to enable Atari environments in Gym/Gymnasium.

This problem of having Gymnasium depend on a fork of a fork of the ALE meant that any changes (such as new environments) or bug fixes that occurred in the ALE were not available in Atari-Py, which included the benchmark for 56 Atari environments that DeepMind first used in their work showing human level performance in the environments. This was made worse by the fact that DeepMind had made their own major modifications and upgrades to the ALE in this time period (some were published publicly in [Xitari](https://github.com/google-deepmind/xitari), some were not). This created well founded scientific reproducibility concerns from the original ALE authors, which led to agreements between the original ALE authors, DeepMind and OpenAI to upstream python bindings from Atari-Py and ALE. Then, Gym would depend directly on the ALE, and DeepMind would contribute all their code to ALE so that the public could use it in a centralized and reproducible way. With the release of Gymnasium 1.0, we're finally completing this process of upstreaming all Atari environments from Gymnasium to ALE.

As a result, Atari documentation has been moved to [ale.farama.org](ale.farama.org) with the Gymnasium links redirecting users. We are maintaining `pip install "gymnasium[atari]"` (though removing `accept-rom-license` as it's unnecessary now) for backward compatibility. Most importantly, the plugin system described previously means that users need to `import ale_py` in order to register environments.

# Looking Ahead
Gymnasium 1.0 brings a refined, clearer, and more efficient framework for creating and interacting with reinforcement learning environments. With a focus on long-term stability, we intend this to be the final breaking change for the foreseeable future. We hope that this release sets the foundation for future growth in the reinforcement learning community.
