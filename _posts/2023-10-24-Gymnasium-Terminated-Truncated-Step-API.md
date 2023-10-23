layout: blog
short_title: "Gymnasium Terminated / Truncated API"
subtitle: "In-depth explanation of the "terminated" and "truncated" values in Gymnasium's Env.step API, and their context in RL theory"
title: "Gymnasium Terminated / Truncated Step API"
date: "2023-10-24"
excerpt: "In this post, we explain the motivation for the `terminated` / `truncated` step API, why alternative implementations were not selected, and the relation to RL theory."
thumbnail: assets/posts/2023-10-24-Gymnasium-Terminated-Truncated-Step-API/banner-gradient-line2.png
image: assets/posts/2023-10-24-Gymnasium-Terminated-Truncated-Step-API/banner-gradient-line2.png
read_time: 6
---
---

## Summary
The `Env.step` API was changed in Gym v26 to use `terminated` and `truncated` instead of a single `done` value.

In Gym versions prior to v25, the step API returned 4 elements:
```python
>>> obs, reward, done, info = env.step(action)
```
In Gym v26, the step API returns 5 elements:
```python
>>> obs, reward, terminated, truncated, info = env.step(action)
>>> done = terminated or truncated
```

In all Gymnasium versions, [`Env.step`](https://gymnasium.farama.org/api/env/#gymnasium.Env.step) returns 5 elements:
```python
>>> obs, reward, terminated, truncated, info = env.step(action)
```

Support for the (old) done step API is provided through Gymnasium's [`EnvCompatibility`](https://gymnasium.farama.org/api/wrappers/misc_wrappers/#gymnasium.wrappers.EnvCompatibility) wrapper, accessible through `gym.make(..., apply_api_compatibility=True)`.

For more information, see Gymnasium's [Compatibility With Gym](https://gymnasium.farama.org/content/gym_compatibility/) documentation.

For a detailed explanation of the changes, reasoning behind them, and context in RL theory, read the rest of this post.

# Terminated / Truncated Step API
In this post, we explain the motivation for the `terminated` / `truncated` API change, why alternative implementations were not selected, and the relation to RL theory.

Note: this post was originally drafted for Gym v26, all usages of `Gym` can be interchanged with `Gymnasium`.


## Introduction
To prevent an agent from wandering in circles forever, not doing anything, and for other practical reasons, Gym lets environments have the option to specify a time limit that the agent must complete the environment within. Importantly, this time limit is outside of the agent’s knowledge as it is not contained within their observations. Therefore, when the agent reaches the time limit, the environment should be reset however **this type of reset should be treated differently from when the agent reaches a goal and the environment ends**. We refer to the first type as **truncation**, when the agent reaches the time limit (maximum number of steps) for the environment, and the second type as **termination**, when the environment state reaches a specific condition (i.e. the agent reaches the goal). For a more precise discussion of how Gym works in relation to RL theory, see the [theory](#theory) section.

The problem is that **most users of Gym have treated termination and truncation as identical**. Gym's step API `done` signal only referred to the fact that the environment needed resetting with `info`, `“TimeLimit.truncation”=True or False` specifying if the cause is `truncation` or `termination`.

This matters for most Reinforcement Learning algorithms [[1]](https://arxiv.org/pdf/1712.00378.pdf) that perform bootstrapping to update the Value function or related estimates (i.e. Q-value), used by DQN, A2C, etc. In the following example for updating the Q-value, the next Q-value depends on if the environment has terminated.
```
If terminated:  # case 1
    Next q-value = reward
Else:  # case 2
    Next q-value = reward + discount factor * max action of the Q (next state, action)

# This can more efficiently be written
Next q-value = reward + (not terminated) * discount factor * max action of the Q(next state, action)
```
This can be seen in Algorithm 1 (Page 5) of the original [DQN paper](https://arxiv.org/abs/1312.5602), however, we noted that this case is often ignored when writing the pseudocode for Reinforcement Learning algorithms.

Therefore, if the environment has truncated and not terminated, case 2 of the bootstrapping should be computed, however, if the case is determined by `done`, this can result in the wrong implementation. **This was the main motivation for changing the step API to encourage accurate implementations, a critical factor for academia when replicating work.**

The reason that most users are unaware of this difference between truncation and termination is that documentation on this issue was missing. As a result, a large amount of tutorial code has incorrectly implemented RL algorithms. This can be seen in the top 4 tutorials found searching google for “DQN tutorial”, [[1]](https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html), [[2]](https://towardsdatascience.com/deep-q-learning-tutorial-mindqn-2a4c855abffc), [[3]](https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial), [[4]](http://seba1511.net/tutorials/intermediate/reinforcement_q_learning.html) (checked 21 July 2022) where only a single website (Tensorflow Agents) implements truncation and termination correctly. Importantly, the reason that Tensorflow Agent does not fall for this issue is that Google has recognised this issue with the Gym `step` implementation and has designed their own API where the `step` function returns the `discount factor` instead of `done`. [See time step code block](https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial#environment).

## Alternative Implementations
While developing this new Step API, a number of developers asked why alternative implementations were not taken. There are four primary alternative approaches that we considered:
* No change: With changes to the documentation alone, it is possible for developers to accurately implement Reinforcement Learning algorithms with termination and truncation. However, due to the prevalence of this misunderstanding within the Reinforcement Learning community (as shown in the short survey of tutorials at the end of the introduction), we are sceptical that solely creating documentation and some blog posts would cause a significant shift within the community to fix the issue in the long term. Therefore, we believe no change would not cause the community to fix the root issue.
* Custom Boolean: It is feasible to replace `done` which is a python bool with a custom bool implementation that can act identically to boolean except in addition encoding the `truncation` information. Similar to this is a proposal to replace `done` as an integer to allow the four possible `termination` and `truncation` states. However, the primary problem with both of these implementations is that it is backwards compatible meaning that (old) done code that is not properly implemented with new custom boolean or integer step API could cause significant bugs to occur. As a result, we believe this proposal could cause significantly more issues.
* Discount factor: For [Deepmind Env](https://github.com/deepmind/dm_env/blob/master/docs/index.md) and [TensorflowAgent](https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial#environment), the `step` function return the `discount_factor` instead of `done`. This allows them to have variable `discount_factors` over an episode and can address the issue with termination and truncation. However, we identify two problems with this proposal. The first is similar to the custom boolean implementation that while the change is backwards compatible this can instead cause assessing if the tutorial code is updated to the new API. The second issue is that Gym provides an API solely for environments, and is agnostic to the solving method. So adding the discount factor would change one of the core Gym philosophies.
* 5 elements: While we agree that our proposed 5-element tuple is not optimal, we believe our proposal is the best for the future. One of the primary reasons is that the change makes assessing if code follows the new or old API easy and avoids the issue of being partially backward compatible allowing new bugs to occur.

## Related Reinforcement Learning Theory
Reinforcement Learning tasks into grouped into two - episodic tasks and continuing tasks. Episodic tasks refer to environments that terminate in a finite number of steps. This can further be divided into Finite-Horizon tasks which end in a *fixed* number of steps and Indefinite Horizon tasks which terminate in an arbitrary number of steps but must end (eg. goal completion, task failure). In comparison, Continuing tasks refer to environments which have *no* end (eg. some control process tasks).

The state that leads to an episode ending in episodic tasks is referred to as a terminal state, and the value of this state is 0. The episode is said to have terminated when the agent reaches this state. All this is encapsulated within the Markov Decision Process (MDP) which defines a task (Environment).

A critical difference occurs in practice when we choose to end the episode for reasons outside the scope of the agent (MDP). This is typically in the form of time limits set to limit the number of timesteps per episode (useful for several reasons - batching, diversifying experience etc.). This kind of truncation is essential in training continuing tasks that have no end, but also useful in episodic tasks that can take an arbitrary number of steps to end. This condition can also be in the form of an out-of-bounds limit, where the episode ends if a robot steps out of a boundary, but this is more due to a physical restriction and not part of the task itself.

We can thus differentiate the reason for an episode ending into two categories - the agent reaching a terminal state as defined under the MDP of the task, and the agent satisfying a condition that is out of the scope of the MDP. We refer to the former condition as termination and the latter condition as truncation.

Note that while finite horizon tasks end due to a time limit, this would be considered a termination since the time limit is built into the task. For these tasks, to preserve the Markov property, it is essential to add information about ‘time remaining’ in the state. For this reason, Gym includes a `TimeObservation` wrapper for users who wish to include the current time step in the agent’s observation.
