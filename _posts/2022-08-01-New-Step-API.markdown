---
layout: blog
title: "New Step API #1"
date:   "2022-08-01"
excerpt: "We have recently changed the Gym Env.step API to return 5 elements instead of 4 elements."
---

## TLDR (Too long didn't read)

In [https://github.com/openai/gym/pull/2752](https://github.com/openai/gym/pull/2752), we have recently changed the Gym `Env.step` API to return 5
elements `(obs, reward, termination, truncation, info)` instead of 4 elements `(obs, reward, done, info)`
where `done = termination or truncation`. For training agents, where `done` was used previously, then `terminated`
should be used.

For a detailed explanation of the changes and reasoning, read the rest of this issue.

# New Step API explanation

In this post, we explain the motivation for the change, what the new `Env.step` API is, why alternative implementations
were not selected and the suggested code changes for developers.

## Introduction

In Gym, to prevent an agent from wandering in circles forever, not doing anything, and for other practical reasons,
environments have the option to specify a time limit for an agent to complete a task. Importantly, this time limit is
outside of the agent’s knowledge as it is not contained within their observations. Therefore, when the agent reaches the
time limit, the environment should be reset however **this type of reset should be treated differently from when the
agent reaches a goal and the environment ends**. We refer to the first type as **truncation** when the agent reaches the
time limit (maximum number of steps) for the environment. The second type is **termination** when the environment state
reaches a specific condition (i.e. the agent reaches the goal). For a more precise discussion of how Gym works in
relation to RL theory, see the [theory](#theory) section.

The problem is that **most users of Gym have treated termination and truncation as identical**. Gym API’s `done` signal
only referred to the fact that the environment needed resetting with `info`, `“TimeLimit.truncation”=True or False`
specifying if truncation or termination.

This matters for most Reinforcement Learning algorithms [[1]](https://arxiv.org/pdf/1712.00378.pdf) that perform
bootstrapping to update the Value function or related estimates (i.e. Q-value), used by DQN, A2C, etc. When computing
the estimated next step Q-value if the environment was terminated or not.

```
If terminated:  # case 1
    Next q-value = reward
Else:  # case 2
    Next q-value = reward + discount factor * max action of the Q (next state, action)
```

This can be seen in Algorithm 1 (Page 5) of the original [DQN paper](https://arxiv.org/abs/1312.5602), however, this is
often ignored when writing the pseudocode for Reinforcement Learning algorithms.

Therefore, if the environment has truncated but not terminated, case 2 of the bootstrapping should be computed however,
if the case is determined by `done` (not `terminated`) this will result in the wrong implementation. **This was the main
motivation for changing the step API to encourage accurate implementations, a critical factor for academia to replicate
work.**

The reason that most users are unaware of this difference between truncation and termination is that documentation on
this issue was missing. As a result, a large amount of tutorial code has incorrectly implemented RL algorithms. This can
be seen in the top 4 tutorials found searching google for “DQN
tutorial”, [1](https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html)
, [2](https://towardsdatascience.com/deep-q-learning-tutorial-mindqn-2a4c855abffc)
, [3](https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial)
, [4](http://seba1511.net/tutorials/intermediate/reinforcement_q_learning.html) (checked 21 July 2022) that includes the
official PyTorch tutorial where only one webiste (Tensorflow Agents) implements truncation and termination correctly.
Importantly, the reason that Tensorflow Agent does not fall for this issue is that Google has recognised this issue with
the Gym step implementation and has designed their own API where the `step` function returns the `discount factor`
instead of `done`. [See time step code block](https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial#environment).

## New Step API

In this Section, we discuss the new step API along with the changes made to Gym that will affect users. We should note
that these changes might not be implemented by python modules or tutorials that use Gym. Between `v0.25` and `v0.26`,
this behaviour will be turned off by default but in `v0.27+`, support for the old step API is provided solely through
the `StepAPICompatibility` wrapper.

<ol>
<li>All existing environment implementations within Gym (i.e., CartPole) have been changed to the new API *without*
direct support for old API. Therefore, be warned if you unwrap an environment, this will cause issues.
However <code>gym.make</code> for any environment will default to adding a compatible wrapper that converts the <code>step</code> function
back to the old API to make the change backwards compatible. This will raise new warnings about the changes but you
can choose to ignore them.<br>

<code># old step API </code><br>
<code>def step(self, action) -> Tuple[ObsType, float, bool, dict]:</code><br>
<code># new step API</code><br>
<code>def step(self, action) -> Tuple[ObsType, float, bool, bool, dict]:</code>

</li>
<li>The Gym Vector environment implementations (<code>AsyncVectorEnv</code> and <code>SyncVectorEnv</code>) are changed to be compatible with
   both and the old API enabled by default. The new API can be enabled by using the newly added
   argument <code>new_step_api=True</code> in the constructor.</li>

<li>All wrapper implementations are changed to be compatible with both the old and the new API with the old API enabled
   by default. To enable the new step API, use <code>new_step_api=True</code> in the constructor of any Gym wrapper.</li>

<li>
Changes in phrasing - In the vector environments, <code>terminal_reward</code>, <code>terminal_observation</code> etc. is replaced
   with <code>final_reward</code>, <code>final_observation</code> etc. The intention is to reserve the 'termination' word for only
   if <code>terminated=True</code>. (for some motivation, Sutton and Barto use terminal states to specifically refer to special
   states whose values are 0, states at the end of the MDP. This is not true for a truncation where the value of the
   final state need not be 0. So the current usage of <code>terminal_obs</code> etc. would be incorrect if we adopt this
   definition)
</li>

</ol>

## Suggested Code changes

We believe there are primarily two changes that will have to be made by developers updating to the new Step API.

<ol>
<li>Stepping through the environment - Within <code>v0.25</code>, the new step API is turned off by default meaning that no code
   changes are required if you don’t use an unwrapped environment (if changes are necessary, please make us aware on
   github or discord). However, you can turn on the new step API in both <code>gym.make</code> and for gym wrappers. When you do
   this, you need to change the <code>env.step</code> to take 5 elements,
   i.e. <code>obs, reward, termination, truncation, info = env.step(action)</code>. To loop through the environment then you need
   to check if the environment needs resetting by checking <code>done = terminated or truncated</code>.<br>


<code>env = gym.make(“CartPole-v1”, new_step_api=True)</code><br>
<code>done = False</code><br>
<code>while not done:</code><br>
<code>&emsp;action = env.action_space.sample()</code><br>
<code>&emsp;obs, reward, terminated, truncated, info = env.step(action)</code><br>
<code>&emsp;done = terminated or truncated</code><br>
</li>
<li>Training with truncation - Using the old step API, then for training reinforcement learning agents should consider if
   the final <code>env.step</code>’s <code>info</code> parameter contains the <code>TimeLimit.truncated=True</code>. If this is true, then for the replay
   buffer, <code>done=False</code> should be used, however, as this is the end of an episode, additional code may be needed. Using
   the code that already implemented the difference between truncated and terminated, then minimal code changes are
   necessary.</li>
</ol>

## Additional changes

The plan is that in v0.27.0, Gym will have the new step API on by default with support primarily given using
the `StepCompatibility` wrapper.

#### `StepAPICompatibility` Wrapper

1. This wrapper is added to support conversion from old to new API and vice versa.
2. Takes `new_step_api` argument in `__init__` that is False by default for the old API.
3. Wrapper applied in `gym.make` with `new_step_api=False` by default. It can be changed during make
   like `gym.make("CartPole-v1", new_step_api=True)`. The order of wrappers applied at make is as follows - core env ->
   PassiveEnvChecker -> StepAPICompatibility -> other wrappers

#### `step_api_compatibility` function

This function is similar to the wrapper, it is used for backward compatibility in wrappers, vector envs. It is used at
interfaces between env / wrapper / vector / outside code. Example usage,

```python
# wrapper's step method
def step(self, action):

    # here self.env.step is made to return in new API, since the wrapper is written in new API
    obs, rew, terminated, truncated, info = step_api_compatibility(self.env.step(action), new_step_api=True) 

    if terminated or truncated:
        print("Episode end")
    ### more wrapper code

    # here the wrapper is made to return in API specified by self.new_step_api, that is set to False by default, and can be changed according to the situation
    return step_api_compatibility((obs, rew, terminated, truncated, info), new_step_api=self.new_step_api) 
```

#### TimeLimit

1. In the current implementation of the timelimit wrapper, the existence of `'TimeLimit.truncated'` key in `info` means
   that truncation has occurred. The boolean value it is set to refer to whether the core environment has already ended.
   So, `info['TimeLimit.truncated']=False`, means the core environment has already terminated. We can
   infer `terminated=True`, `truncated=True` from this case.
2. To change old API to new, the compatibility function first checks info. If there is nothing in info, it
   returns `terminated=done` and `truncated=False` as there is no better information available. If TimeLimit info is
   available, it accordingly sets the two bools.

#### Backward Compatibility

The PR attempts to achieve almost complete backward compatibility. However, there are cases which haven't been included.
Environments directly imported eg. `from gym.envs.classic_control import CartPoleEnv` would not be backward compatible
as these are rewritten in new API. `StepAPICompatibility` wrapper would need to be used manually in this case.
Environments made through `gym.make` all default to old API. Vector and wrappers also default to old API. These should
all continue to work without problems. But due to the scale of the change, bugs are expected.

#### Warning Details

Warnings are raised at the following locations:

1. `gym.Wrapper` constructor - warning raised if `self.new_step_api==False`. This means any wrapper that does not
   explicitly pass `new_step_api=True` into super() will raise the warning since `self.new_step_api=False` by default.
   This is taken care of by wrappers written inside gym. Third-party wrappers will face a problem in a specific
   situation - if the wrapper is not impacted by step API. eg. a wrapper subclassing ActionWrapper. This would work
   without any change for both APIs, however, to avoid the warning, they still need to pass `new_step_api=True` into
   super(). The thinking is - "If your wrapper supports the new step API, you need to pass `new_step_api=True` to avoid
   the warning".
2. `PassiveEnvChecker`, `passive_env_step_check` function - if step return has 4 items a warning is raised. This happens
   only once since this function is only run once after env initialization. Since `PassiveEnvChecker` is wrapped first
   before step compatibility in `gym.make`, this will raise a warning based on the core env implementation's API.
3. `gym.VectorEnv` constructor - warning raised if `self.new_step_api==False`.
4. `StepAPICompatibility` wrapper constructor - the wrapper that is applied by default at `gym.make`.
   If `new_step_api=False`, a warning is raised. This is independent of whether the core env is implemented in the new
   or old API and only depends on the `new_step_api` argument.

## Alternative Implementations

While developing this new Step API, a number of developers asked why alternative implementations were not taken. There
are four primary alternative approaches that we considered:

* No change: With changes to the documentation alone, it is possible for developers to accurately implement
  Reinforcement Learning algorithms with termination and truncation. However, due to the prevalence of this
  misunderstanding within the Reinforcement Learning community (as shown in the short survey of tutorials at the end of
  the introduction), we are sceptical that solely creating documentation and some blog posts there would be a
  significant shift within the community to fix the issue in the long term. Therefore, we believe no change would not
  cause the community to fix the issue.
* Custom Boolean: It is feasible to replace `done` which is a python bool with a custom bool implementation that can act
  identically to boolean except in addition to encoding the `truncation` information. Similar to this, is a proposal to
  replace `done` as an integer to allow the four possible `termination` and `truncation` states. However, the primary
  problem with this implementation is that it is backwards compatible meaning that old code that is not properly
  implemented with new custom boolean or integer step API could cause significant bugs to occur. As a result, we believe
  this proposal could be even more breaking than our actual proposed changes.
* Discount factor: For [Deepmind Env](https://github.com/deepmind/dm_env/blob/master/docs/index.md)
  and [TensorflowAgent](https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial#environment), the `step` function
  return the `discount_factor` instead of `done`. This allows them to have variable `discount_factors` over an episode
  and can address the issue with termination and truncation. However, we identify two problems with this proposal, the
  first is similar to the custom boolean implementation where while the change is backwards compatible this can instead
  cause issues as it is difficult to assess if the code is updated to the new API. The second issue is more about the
  goal of Gym. As Gym provides an API solely for environments / MDP, making it agnostic to the solver however adding the
  discount factor, starts to move Gym away from a pure environment API.
* 5 elements: While we agree that our proposed 5-element tuple is not optimal (there are many things like this in Gym
  which if developed in 2022 with the goal of making a de facto standard for Reinforcement Learning environment API
  would change), we believe our proposal is the best for the future. The reason for this is that it is clear if an
  algorithm is following the new or old step API from the code.

## Theory

We can categorize Reinforcement Learning tasks into two categories - episodic tasks and continuing tasks. Episodic tasks
refer to tasks that end in a finite number of steps. This can further be divided into Finite-Horizon tasks which end in
a *fixed* number of steps and Indefinite Horizon tasks which end in an arbitrary number of steps but must end (eg. goal
completion, task failure). Continuing tasks refer to tasks which have *no* end (eg. some control process tasks). The
state that leads to an episode ending in episodic tasks is referred to as a terminal state, and the value of this state
is 0. The episode is said to have terminated when the agent reaches this state. All this is encapsulated within the
Markov Decision Process (MDP) which defines the task.

A critical difference occurs in practice when we choose to end the episode for reasons outside the scope of the MDP.
This is typically in the form of time limits set to limit the number of timesteps per episode (useful for several
reasons - batching, diversifying experience etc.). This kind of truncation is essential in training continuing tasks
that have no end, but also useful in episodic tasks that can take an arbitrary number of steps to end. This condition
can also be in the form of an out-of-bounds limit, where the episode ends if a robot steps out of a boundary, but this
is more due to a physical restriction and not part of the task itself.

We can thus differentiate the reason for an episode ending into two categories - the agent reaching a terminal state as
defined under the MDP of the task, and the agent satisfying a condition that is out of the scope of the MDP. We refer to
the former condition as termination and the latter condition as truncation.

Note that while finite horizon tasks end due to a time limit, this would be considered a termination since the time
limit is built into the task. For these tasks, to preserve the Markov property, it is essential to add information about
‘time remaining’ in the state. For this reason, Gym includes a `TimeObservation` wrapper for users who wish to include
the current time step in the agent’s observation.
