---
layout: blog
short_title: "Deep Dive: VectorEnv Autoreset"
subtitle: "In-depth explanation of autoreset Modes in Gymnasium Vector Environments"
title: "Deep Dive: Autoreset Modes in Gymnasium v1.1 Vector Environments"
date: "2025-02-20"
excerpt: "Autoreset control when vectorised environment reset sub-environments on terminations or truncations. Gymnasium offers three options, for which, we present descriptions and examples for each."
Author: "Mark Towers"
thumbnail:
image:
read_time: 3
---

# Summary

In Gymnasium v1.0, significant changes were made to improve the `VectorEnv` implementation. One of these changes is how sub-environments are reset on termination (or truncation), referred to as the Autoreset Mode or API. Added in Gymnasium v1.1, Gymnasium's built-in Vector environments and wrappers support for all autoreset modes / APIs, though the default with `make_vec` is next-step. In this blog post, we explain the differences in the possible modes and how to use them with example training code for each.

## Autoreset Modes

Vector environments allow multiple sub-environments to run in parallel, improving training efficiency in Reinforcement Learning through sampling multiple episodes at the same time. What should the vector environment do when one or multiple sub-environments reset as it will need to be reset before future actions can be taken? There are three options referred to as Next-Step, Same-Step and Disabled mode, visualised in the figure below.

Gymnasium's built-in vector environment implementations, `SyncVectorEnv` and `AsyncVectorEnv` support all three modes using the `autoreset_mode` argument expecting a `gym.vector.AutoresetMode`, for example, `SyncVectorEnv(..., autoreset_mode=gym.vector.AutoresetMode.NEXT_STEP)`. Further, most of Gymnasium's vector wrappers support all modes, however, for external projects, there is no guarantee what autoreset mode will be supported by either the vector environments, wrapper implementations or training algorithms. To help users know what autoreset mode is being used, `VectorEnv.metadata["autoreset_mode"]` should be specified and that developers can specify in their documentation what autoreset modes are supported.

![Flowchart diagram representing the different autoreset modes](assets/images/blogs/autoreset-modes.svg)

For Gymnasium, some of the vector wrappers only support particular autoreset modes.

<table style="border-collapse: collapse; width: 100%;">
  <tr>
    <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Vector Wrapper name</th>
    <th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Next step</th>
    <th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Same Step</th>
    <th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Disabled</th>
  </tr>
  <tr>
    <td style="border: 1px solid #ddd; padding: 8px;"><code>VectorObservationWrapper</code></td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10004;</td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10006;</td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10004;</td>
  </tr>
  <tr>
    <td style="border: 1px solid #ddd; padding: 8px;"><code>TransformObservation</code></td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10004;</td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10006;</td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10004;</td>
  </tr>
  <tr>
    <td style="border: 1px solid #ddd; padding: 8px;"><code>NormalizeObservation</code></td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10004;</td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10006;</td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10006;</td>
  </tr>
  <tr>
    <td style="border: 1px solid #ddd; padding: 8px;"><code>VectorizeTransformObservation</code>*</td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10004;</td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10004;</td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10004;</td>
  </tr>
  <tr>
    <td style="border: 1px solid #ddd; padding: 8px;"><code>RecordEpisodeStatistics</code></td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10004;</td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10004;</td>
    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">&#10004;</td>
  </tr>
</table>

\* all inherited wrappers from `VectorizeTransformObservation` are compatible (`FilterObservation`, `FlattenObservation`, `GrayscaleObservation`, `ResizeObservation`, `ReshapeObservation`, `DtypeObservation`).

### Next-Step Mode
If a sub-environments terminates, in the next step call, it is reset. Gymnasium's Async and Sync Vector environments default to this mode. Implementing training algorithms using Next-step mode, beware of episode boundaries in training, either through not adding the relevant data to the replay buffer or through masking out the relevant errors in rollout buffers.

<details>
<summary><b>Click for Example training code</b></summary>

<div class="language-python highlighter-rouge">
<div class="highlight">
<pre class="highlight"><code>
import gymnasium as gym
from collections import deque

# Initialize environment and buffer
envs = gym.make_vec("CartPole-v1", num_envs=2, vector_kwargs={"autoreset_mode": gym.vector.AutoresetMode.SAME_STEP})
replay_buffer = deque(maxlen=100)

observations, _ = envs.reset()
while True:   # Training loop
    actions = policy(observations)
    next_observations, rewards, terminated, truncated, infos = envs.step(actions)

    # Add to replay buffer
    for i in range(envs.num_envs):
        # Get actual next observation
        if terminated[i] or truncated[i]:
            actual_next_obs = infos["final_obs"][i]
        else:
            actual_next_obs = next_observations[i]

        replay_buffer.append((observations[i], actions[i], rewards[i], terminated[i], actual_next_obs))

    observations = next_observations  # Update observation
</code></pre>
</div>
</div>

</details>

### Same-Step Mode
If a sub-environments terminated, in the same step call, it is reset, beware that some vector wrappers do not support this mode and the step's observation can be the reset's observation with the terminated observation being stored in `info["final_obs"]`. This makes it is a simplistic approach for training algorithms if value errors with truncation are skipped. See [this](https://farama.org/Gymnasium-Terminated-Truncated-Step-API), for details.

<details>
<summary><b>Click for Example training code</b></summary>

<div class="language-python highlighter-rouge">
<div class="highlight">
<pre class="highlight"><code>
import gymnasium as gym
import numpy as np
from collections import deque

# Initialize environment, buffer and episode_start
 envs = gym.make_vec("CartPole-v1", num_envs=2, autoreset_mode=gym.vector.AutoresetMode.NEXT_STEP)
 replay_buffer = deque(maxlen=100)
 episode_start = np.zeros(envs.num_envs, dtype=bool)

 observations, _ = envs.reset()
 while True:   # Training loop
     actions = policy(observations)
     next_observations, rewards, terminations, truncations, infos = envs.step(actions)

     # Add to replay buffer
     for i in range(envs.num_envs):
         if not episode_start[i]:
             replay_buffer.append((observations[i], actions[i], rewards[i], terminations[i], next_observations[i]))

     # update observation and if episode starts
     observations = next_observations
     episode_start = np.logical_or(terminations, truncations)
</code></pre>
</div>
</div>

</details>

### Disabled Mode
No automatic resetting occurs and users need to manually reset the sub-environment through a mask, `env.reset(options={"mask": np.array([True, False, ...], dtype=bool)})`. The easier way of generating this mask is `np.logical_or(terminations, truncations)`. This makes training code closer to single vector training code, however, can be slower is some cases due to running additional functions.

<details>
<summary><b>Click for Example training code</b></summary>

<div class="language-python highlighter-rouge">
<div class="highlight">
<pre class="highlight"><code>
import gymnasium as gym
import numpy as np
from collections import deque

# Initialize environment, buffer and episode_start
envs = gym.make_vec("CartPole-v1", num_envs=2, autoreset_mode=gym.vector.AutoresetMode.DISABLED)
replay_buffer = deque(maxlen=100)

observations, _ = envs.reset()
while True:   # Training loop
    actions = policy(observations)
    next_observations, rewards, terminations, truncations, infos = envs.step(actions)

    # Add to replay buffer
    for i in range(envs.num_envs):
        replay_buffer.append((observations[i], actions[i], rewards[i], terminations[i], next_observations[i]))

    # update observation
    autoreset = np.logical_or(terminations, truncations)
    if np.any(autoreset):
        observations = envs.reset(options={mask: autoreset})
    else:
        observations = next_observations
</code></pre>
</div>
</div>

</details>

## Conclusion
The autoreset mode have a significant impact on the implementation of RL training algorithms for sampling from environments and its not possible to convert between different modes. Gymnasium v1.1 now supports all three autoreset implementations with most of the wrappers supporting all of them providing more options to developers and greater backward compatibility to Gymnasium v0 vectorised training algorithms.

If there are missing details or questions please raise them on the [Farama Discord](https://discord.gg/bnJ6kubTg6) or [GitHub](https://github.com/farama-Foundation/gymnasium).
