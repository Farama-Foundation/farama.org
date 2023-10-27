---
layout: blog
short_title: "Deep Dive: Gymnasium Step API"
subtitle: "In-depth explanation of the terminated and truncated values in Gymnasium's Env.step API"
title: "Deep Dive: Gymnasium Terminated - Truncated Step API"
date: "2023-10-23"
excerpt: "In this post, we explain the motivation for the terminated / truncated step API, why alternative implementations were not selected, and the relation to RL theory."
thumbnail: assets/posts/2023-10-24-Gymnasium-Terminated-Truncated-Step-API/banner-gradient-line2.png
image: assets/posts/2023-10-24-Gymnasium-Terminated-Truncated-Step-API/banner-gradient-line2.png
read_time: 6
---

## Summary
The `Env.step` function definition was changed in Gym v0.26  and for all Gymnasium versions from using `done` in favour of using `terminated` and `truncated`. 

In Gym versions before v0.25, `Env.step` returned 4 elements:
```python
>>> obs, reward, done, info = env.step(action)
```
This was changed in Gym v0.26 and for all Gymnasium versions to return 5 elements:
```python
>>> obs, reward, terminated, truncated, info = env.step(action)
>>> done = terminated or truncated
```

Gym v26 and Gymnasium still provide support for environments implemented with the `done` style step function with the [Shimmy Gym v0.21 environment](https://shimmy.farama.org/environments/gym/#shimmy.openai_gym_compatibility.GymV21CompatibilityV0). For more information, see Gymnasium's [Compatibility With Gym](https://gymnasium.farama.org/content/gym_compatibility/) documentation.

For a detailed explanation of the changes, the reasoning behind them, and the context within RL theory, read the rest of this post.

# Terminated / Truncated Step API
In this post, we explain the motivation for the `terminated`-`truncated` step API, why alternative implementations were not selected, and the relation to RL theory.

Note: this post was originally drafted for Gym v26, all usages of `Gym` can be interchanged with `Gymnasium`.

## Introduction
To prevent an agent from wandering in circles forever, not doing anything, and for other practical reasons, Gym lets environments have the option to specify a time limit that the agent must complete the environment within. Importantly, this time limit is outside of the agent’s knowledge as it is not contained within their observations. Therefore, when the agent reaches this time limit, the environment should be reset but **should not be treated the same as if the agent reaches a goal and the environment ends**. We refer to the first type as **truncation**, when the agent reaches the time limit (maximum number of steps) for the environment, and the second type as **termination**, when the environment state reaches a specific condition (i.e. the agent reaches the goal). For a more precise discussion of how Gym works in relation to RL theory, see the [theory](#theory) section.

The problem is that **most users of Gym have treated termination and truncation as identical**. Gym's step API `done` signal only referred to the fact that the environment needed resetting with `info[“TimeLimit.truncation”]` specifying if the cause is `truncation` or `termination`. However, we found a large number of implementations were not aware of this critical information and treated `done` as identical in all situations. 

This matters as most Reinforcement Learning algorithms [[1]](https://arxiv.org/pdf/1712.00378.pdf) perform bootstrapping to update the Value function or related estimates (i.e. Q-value), used by DQN, PPO, etc as target bootstrap value is dependent on if and only if the environment has **terminated** (not truncated). Therefore using `done` uniformly would result in an incorrect loss function. **This was the main motivation for changing the step API to encourage accurate implementations, a critical factor in academia for replicating work.**
```
If terminated:  # case 1
    Next q-value = reward
Else:  # case 2
    Next q-value = reward + discount factor * max action of the Q (next state, action)

# This can more efficiently be written
Next q-value = reward + (not terminated) * discount factor * max action of the Q(next state, action)
```
This update function can be seen in Algorithm 1 (Page 5) of the original [DQN paper](https://arxiv.org/abs/1312.5602), however, we should note that this case is often ignored in pseudocode for Reinforcement Learning algorithms.

The reason that most users are unaware of the difference between truncation and termination is that documentation on this issue was missing. As a result, a large amount of tutorial code has incorrectly implemented RL algorithms. This can be seen in the top 4 tutorials found searching google for “DQN tutorial”, [[1]](https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html), [[2]](https://towardsdatascience.com/deep-q-learning-tutorial-mindqn-2a4c855abffc), [[3]](https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial), [[4]](http://seba1511.net/tutorials/intermediate/reinforcement_q_learning.html) (checked 21 July 2022) where only a single website (Tensorflow Agents) implements truncation and termination correctly. Importantly, the reason that Tensorflow Agent does not fall for this issue is that Google has recognised this issue with the Gym `step` implementation and has designed their own API where the `step` function returns the `discount factor` instead of `done`. [See time step code block](https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial#environment).

## Alternative Implementations
While developing this new Step API, several developers asked why alternative implementations were not taken. We identified four general approaches to solve this issue that we considered:
* No code change: With changes to the documentation alone, it is possible for developers to accurately implement Reinforcement Learning algorithms with termination and truncation. However, due to the prevalence of this misunderstanding within the Reinforcement Learning community (as shown in the short survey of tutorials at the end of the introduction), we are sceptical that solely creating documentation and some blog posts would cause a significant shift within the community to fix the issue in the long term. Therefore, we believe no change would be too slow to fix the issue.
* Custom Boolean: It is feasible to replace `done` which is a Python bool with a custom bool implementation that can act identically to a boolean except in addition encoding the `truncation` information. Similar to this is a proposal to replace `done` as an integer to allow the four possible `termination` and `truncation` states. However, the primary problem with both of these implementations is that **it is** backwards compatible meaning that (old) done code that is not properly implemented with new custom boolean or integer step API could cause significant bugs to occur without the user being aware of the change. As a result, we believe this proposal could cause significantly more issues to the community.
* Discount factor: For [Deepmind Env](https://github.com/deepmind/dm_env/blob/master/docs/index.md) and [TensorflowAgent](https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial#environment), the `step` function return the `discount_factor` instead of `done`. This allows them to have variable `discount_factors` over an episode and can address the issue with termination and truncation. However, we identify two problems with this proposal. The first is similar to the custom boolean implementation in that while the change is backwards compatible this can instead cause assessing if the tutorial code is updated to the new API. The second issue is that Gym provides an API solely for environments, and is agnostic to the solving method. So adding the discount factor would change one of the core Gym philosophies.
* 5 elements: While we agree that our proposed 5-element tuple is not optimal, we believe our proposal is the best for the future. One of the primary reasons is that the change makes assessing if code follows the new or old API easy and avoids the issue of being partially backwards compatible allowing new bugs to occur. While this change does require updating code, such a change, we hope, will cause users to fix their code if previously incorrect.  

## Related Reinforcement Learning Theory
Reinforcement Learning tasks can be grouped into two types - episodic tasks and continuing tasks. Episodic tasks refer to environments that terminate in a finite number of steps. This can further be divided into Finite-Horizon tasks which end in a *fixed* number of steps and Indefinite-Horizon tasks which terminate in an arbitrary number of steps but must end (eg. goal completion, task failure). In comparison, Continuing tasks refer to environments which have *no* end (eg. some control process tasks).

The state that leads to an episode ending in episodic tasks is referred to as a terminal state, and the value of this state is 0. The episode is said to have terminated when the agent reaches this state. All this is encapsulated within the Markov Decision Process (MDP) which defines a task (`Env` within Gym).

A critical difference occurs in practice when we choose to end the episode for reasons outside the scope of the agent (MDP). This is typically in the form of time limits set to limit the number of timesteps per episode (useful for several reasons - batching, diversifying experience, etc.). This kind of truncation is essential in training continuing tasks that have no end, but also useful in episodic tasks that can take an arbitrary number of steps to end. This condition can also be in the form of an out-of-bounds limit, where the episode ends if a robot steps out of a boundary, but this is more due to a physical restriction and not part of the task itself.

We can thus differentiate the reason for an episode ending into two categories - the agent reaching a terminal state as defined under the MDP of the task, and the agent satisfying a condition that is out of the scope of the MDP. We refer to the former condition as termination and the latter condition as truncation.

Note that while finite horizon tasks end due to a time limit, this would be considered a termination since the time limit is built into the task. For these tasks, to preserve the Markov property, it is essential to add information about ‘time remaining’ in the state. For this reason, Gym includes a `TimeObservation` wrapper for users who wish to include the current time step in the agent’s observation.
