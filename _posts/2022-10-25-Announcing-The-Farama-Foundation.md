---
layout: blog
title: "Announcing The Farama Foundation"
date: "2022-10-25"
excerpt: "Today we’re announcing the Farama Foundation – a new nonprofit organization designed in part to house major existing open source reinforcement learning (“RL”) libraries in a neutral nonprofit body."
thumbnail: assets/images/farama_placeholder.png
---

## Introduction

Today we’re announcing the Farama Foundation – a new nonprofit organization designed in part to house major existing open source reinforcement learning (“RL”) libraries in a neutral nonprofit body. We aim to provide standardization and long term maintenance to these projects, as well as improvements to their reproducibility, performance, and quality of life features. We are also working to develop key pieces of missing software for the open source reinforcement learning ecosystem.

Our mission is to develop and maintain open source reinforcement learning tools, making reinforcement learning research faster and more productive, and reducing the engineering workload required to apply RL in both research and industry.

This post explains who we are, what we’re working on right now, and what our long term goals and vision are. This post also publicly announces the release of [Gymnasium](https://github.com/Farama-Foundation/Gymnasium), a library where the future maintenance of OpenAI Gym will be taking place.


## Reinforcement Learning Tooling and Environments

Reinforcement learning is a popular approach to AI where an agent learns to take sequential actions in an environment through trial and error. In practice, environments are most often a piece of software like a game or simulation, but [the real world works too](https://gym.offworld.ai/). Reinforcement learning has been able to achieve human level performance, or better, in a wide variety of tasks such as [controlling robots](https://www.youtube.com/watch?v=x4O8pojMF0w), [playing games](https://www.youtube.com/watch?v=WXuK6gekU1Y), or [automating industrial processes](https://www.nature.com/articles/s41586-021-04301-9). Reinforcement learning has also been responsible for some of the greatest achievements of AI in recent history, such as [AlphaGo](https://www.youtube.com/watch?v=WXuK6gekU1Y), [AlphaStar](https://www.deepmind.com/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii), and [DOTA2](https://openai.com/five/).

Reinforcement learning is conceptualized as a loop where the agent observes the state of its environment, and then takes an action that alters that state. At the time of receiving the next observation, the agent also receives a reward associated with the most recent action. This process continues in a cycle, and during learning the agent seeks to maximize its expected average reward . Here’s a visualization of this cycle:

<center>
<img src="/assets/posts/2022-10-25-Announcing-The-Farama-Foundation/image1.png" alt="Reinforcement Learning loop" width="400"/>
</center>

In supervised learning, the basic software stack typically only has three components: the dataset, preprocessing of the dataset, and the deep learning library. In reinforcement learning, the software stack is much more complex. It starts with constructing the environment itself, usually a piece of software like a simulation or a video game. The base environment logic is then wrapped with an API that learning code can be applied to.

Depending on how the reinforcement learning algorithm interacts with the environment, preprocessing wrappers are then applied (e.g. to make image observations greyscale). Only after all of this is done can a reinforcement learning algorithm be applied, which are typically implemented using deep learning tools (e.g. PyTorch, TensorFlow, Jax). A comparison of both software stacks is shown in the simplest form below:

<center>
<img src="/assets/posts/2022-10-25-Announcing-The-Farama-Foundation/image2.png" alt="Software Stacks" width="400" />
</center>

## The Environment Problem for Researchers

Reinforcement learning’s reliance on standard software environments as opposed to datasets creates a lot of unique problems for the field. Given a piece of image classification code, you can give any sufficiently large labeled image dataset to it, press run, and it will mostly work. Unlike datasets, when you’re dealing with software based environments like games, you have to make sure the environment runs on your operating system and CPU architecture, is bug-free, runs with modern versions of the underlying tools (e.g. a current version of Python), and has an API that is compatible with your learning code. You’d also like it to have documentation, be available for installation via package manager, and have specialized reproducibility features.

Previously, RL environment projects have been maintained and owned on GitHub by separate groups or individuals. This means that if someone suddenly quits, burns out or [gets hit by a bus](https://en.wikipedia.org/wiki/Bus_factor), or a company goes under, maintenance completely stops. Even the standard open source approach of someone forking the environment is undesirable here, because everyone needs to use the exact same version of an environment for reproducibility and consistency across the research field.

Beyond the quality of life, reproducibility, and productivity issues this creates for researchers, the reality is that as long as the field of reinforcement learning exists, standard maintained environments that can allow for performance comparisons are needed. Our long term solution to this problem is to have the repositories be managed by a unified neutral nonprofit organization, akin to the Linux Foundation or Apache Software Foundation, that maintains the libraries over time and brings them into compliance with a unified and consistent [set of standards](https://farama.org/project_standards). This is a large part of what Farama was created to accomplish.


## The Standard API Problem and The Origins of The Farama Foundation

In order to have standardized environments and modular RL code in general, there needs to be a well-designed and easy to use standard API for accessing reinforcement learning environments. For most use cases, this already exists through a Python library called Gym. Gym was originally created by OpenAI 6 years ago, and it includes a standard API, tools to make environments comply with that API, and a set of assorted reference environments that have become very widely used benchmarks. It’s been installed more than [43 million times](https://pepy.tech/project/gym) via pip, cited more than [4,500 times](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=itSa94cAAAAJ&citation_for_view=itSa94cAAAAJ:HbR8gkJAVGIC) on Google Scholar, and is used by more than [32,000 projects](https://github.com/openai/gym/network/dependents) on GitHub. This makes it by far the most used RL library in the world.

The Farama Foundation effectively began with the development of [PettingZoo](https://github.com/Farama-Foundation/PettingZoo), which is basically Gym for multi-agent environments. PettingZoo was developed over the course of a year by 13 contributors. Amongst other things, its development involved the standardization or creation of about 60 environments, including [adding support to the ALE for multi-player Atari games for the first time](https://github.com/Farama-Foundation/Multi-Agent-ALE). PettingZoo was released in late 2020 and is now used widely, with 850,000 installations via pip, making it the third most installed RL library in the world.

Gym did a lot of things very well, but OpenAI didn’t devote substantial resources to it beyond its initial release. The maintenance of Gym gradually decreased until Gym became wholly unmaintained in late 2020. In early 2021, OpenAI gave us control over the Gym repository.

Since then, much more development has occurred than in the previous 5 years following its release. Our updates to Gym included changing the core API to resolve long standing issues with the design (a blog post on this is coming soon), creating a full-fledged [documentation website](https://www.gymlibrary.dev/) for the first time ever, adding a compliance checker for the API, fixing massive bugs across every surface of the code base (when we took over, even installation didn’t work correctly in many cases), removing several dependencies on long deprecated software, and [much more](https://github.com/openai/gym/releases).

The core [team](https://farama.org/team) of contributors maintaining Gym and PettingZoo dramatically grew into a massive international team, and our greater group of contributors, now known as the Farama Foundation, currently spans 14 timezones. Having standard APIs like Gym and PettingZoo be well-maintained and stabilized in a neutral nonprofit body is very important for the field, and is a prerequisite for standardizing environment libraries.


## Gymnasium

This brings us to [Gymnasium](https://github.com/Farama-Foundation/Gymnasium). It's essentially just our fork of Gym that will be maintained going forward. It can be trivially dropped into any existing code base by replacing `import gym` with `import gymnasium as gym`, and Gymnasium 0.26.2 is otherwise the same as Gym 0.26.2.

Even for the largest projects, upgrading is trivial as long as they’re up-to-date with the latest version of Gym. We’re doing this so that the API an entire field depends on can be maintained in a neutral entity long term, and to give us access to additional permissions so we can have a more productive and sustainable development and release workflow. It’s our understanding that OpenAI has no plans to develop Gym going forward, so this won’t create a situation where the community becomes divided by two competing libraries.

Right now, Gymnasium is live and you can install it with the usual `pip install gymnasium`. The documentation website is available [here](https://gymnasium.farama.org/) and we encourage users to begin upgrading (if you’re already on the newest version of Gym, this should be trivial). Many large projects have already agreed to upgrade to Gymnasium in the near future, such as [CleanRL](https://github.com/vwxyzjn/cleanrl) and [Stable Baselines 3](https://github.com/DLR-RM/stable-baselines3).

You can view the development roadmap for Gymnasium [here](https://github.com/Farama-Foundation/Gymnasium/issues/12), though it’s basically the same as before. We have no plans for further breaking changes to the core API, and we’ll mainly be focusing on upgrades to vectorized environments and reimplementing all the built-in environments in Gymnasium to be able to run on accelerator hardware like GPUs, changes which represent a potential environment speed up of 10x and 1000x respectively. We hope these changes will make reinforcement learning much more accessible in education and allow for researchers to experiment with new ideas much faster.


## Our Other Environments

Beyond PettingZoo and Gymnasium, we’ve already begun officially maintaining several other popular benchmark environments. These include [MAgent2](https://github.com/Farama-Foundation/MAgent2), [D4RL](https://github.com/Farama-Foundation/D4RL), [Minigrid](https://github.com/Farama-Foundation/Minigrid) (formerly gym-minigrid), [Miniworld](https://github.com/Farama-Foundation/MiniWorld) (formerly gym-miniworld), [MiniWoB++](https://github.com/Farama-Foundation/miniwob-plusplus) and [MicroRTS](https://github.com/Farama-Foundation/MicroRTS)/[MicroRTS-Py](https://github.com/Farama-Foundation/MicroRTS-Py) (formerly gym-microrts). You can view these and all of our other projects on our [projects page](https://farama.org/projects).

We’re also currently in discussions with a number of other popular open source reinforcement learning environment libraries about bringing them in, and thus far the discussions have been overwhelmingly positive. If you’re the owner of a widely-used piece of RL software that you think should be part of the Farama Foundation and haven’t already heard from us, please reach out to us at [contact@farama.org](mailto:contact@farama.org).

Our goal is to offer long term maintenance, standardize environments and add key quality of life features. Some of the most important quality of life features we’re working to add are consistent detailed documentation websites (like the ones we created for [Gymnasium](https://gymnasium.farama.org/), [PettingZoo](https://pettingzoo.farama.org/), [Minigrid](https://minigrid.farama.org/) and [Gymnasium-Robotics](https://robotics.farama.org/)), easy installation, support for multiple architectures and operating systems, type hinting, docstrings, and improved rendering functionality. You can read our full list of standards [here](https://farama.org/project_standards.html). We’ve been classifying our [projects](https://farama.org/projects) into two classes – “Mature” projects that comply with these standards, and “Incubating” projects that we’re still actively working to bring up to our standards.


## Our Vision for the Future of RL Tooling

Supervised deep learning is used so often in our daily lives that it’s hard to comprehend. Seemingly every company and every product uses it, and our phones have included [chips dedicated to it](https://gizmodo.com/what-do-the-ai-chips-in-new-smartphones-actually-do-1820913665) for over 5 years. Incredible projects can be done easily by a single person in a fairly short period of time (e.g. [building a face tracking AI for a drone in under a week with a small datasets](https://github.com/Jabrils/TelloTV)).

Reinforcement learning, on the other hand, is rarely used in application right now, and usually requires massive teams to deploy. The vast majority of the work on reinforcement learning is devoted to algorithmic research, but it’s our view that the barrier to reinforcement learning becoming widely used is not primarily an algorithm problem. Current reinforcement learning algorithms can already control [nuclear fusion reactors](https://www.nature.com/articles/s41586-021-04301-9), [robot balloons in the stratosphere](https://www.nature.com/articles/s41586-020-2939-8), [real F-16s fighter jets in flight](https://defbrief.com/2021/03/28/darpa-plans-to-have-ai-fly-an-actual-plane-in-a-dogfight-by-2023/), or [layout production semiconductor chips](https://www.nature.com/articles/s41586-021-03544-w). Reinforcement learning can also achieve superhuman performance in what are extremely challenging games such as [StarCraft 2](https://www.nature.com/articles/s41586-019-1724-z), [DOTA 2](https://www.nature.com/articles/s41586-019-1724-z), [Go](https://www.nature.com/articles/nature24270), [Stratego](https://arxiv.org/pdf/2206.15378.pdf), or [Gran Turismo Sport on real PS4s](https://arxiv.org/abs/2008.07971).

These projects show that current algorithms clearly are capable of incredible feats. However, those projects all generally had teams with more than 15 specialized, highly technically skilled members. Similar projects in supervised machine learning require a fraction of the resources due to readily available and compatible tooling.** _This means that the barrier to reinforcement learning seeing widespread deployment is a tooling problem._** Our long term vision is to solve it.

We believe it is critical for the field that the tools researchers use function well and have long term support. As the initial wave of cleaning up the key benchmark environments passes, we want to turn our focus to developing a set of standardized and widely applicable tools with the intention of making reinforcement learning as easy as supervised learning. We want to make tools that “just work.” If we succeed, this could result in automation for a profoundly greater scope of tasks than anything before, including manufacturing, household devices and robots, automating menial computer tasks, and medical devices like insulin pumps. Our grand vision for our work is to essentially make “RLOps” a thing the way that MLOps is, and make deploying RL feasible for small teams and students.


## Our Future Projects

These are the projects we plan to work on in the pursuit of making RL require less developer labor to deploy into real world applications:

1. Work with video game developers to compile gameplay from real users into the largest offline RL dataset ever created, and publicly release it so that GPT-for-RL styled projects can be attempted. (If you’re a video game developer and are interested in working with us on this – [jkterry@farama.org](mailto:jkterry@farama.org)).
2. Create a standard offline RL dataset format and repository. Development on this has begun – see [Kabuki](https://github.com/Farama-Foundation/Kabuki) – and it will be integrated into all environments we manage.
3. Create good C APIs and tools, so that RL can be more easily deployed in applications like embedded systems or robots.
4. Create a learning library that would hopefully be the first widely used library that “just works,” even in complex and real world applications, including support for distributed computing. This is _by far_ the most ambitious task on this list and deserves its own blog post.


## Donations

Farama has accomplished everything we’ve described above with entirely volunteer contributions. We’re looking for donations to allow our key developers to become full time employees, especially our team members managing other contributors.

Full time staff would make the development and maintenance of our projects more sustainable, let us bring environments to a mature state faster, and give us the capacity to manage many more environments. It would also let us release important new features faster, like making all of the environments in Gymnasium hardware accelerated by default, and give us the manpower to pursue the majority of our future project goals, like a GPT-for-RL enabling dataset.

We’re a 501c3 nonprofit in the United States, so donations to us are tax deductible. We have various [perks](https://farama.org/donations) for individuals or companies who donate larger sums. Our work has the capability to make engineers and researchers in industry and academia alike substantially more productive and make entirely new things feasible to accomplish, as well as dramatically lowering the barrier for new students entering the field.  If you want to see our vision come to light, please [donate](https://farama.org/donations) to the future of AI.


## Contributing

If you are interested in contributing your time to working on projects with the Farama Foundation, we would love to have you. The general process is to join our [discord server](https://discord.gg/PfR7a79FpQ) where we coordinate all development, post a message with your experience and what you’re looking to do, and our project managers will work with you to get you started.


## Final Notes

More than anything, we want to thank our team and community of contributors. Without their immense amount of work and dedication over the past year, truly none of this would’ve been possible.

If you’d like to meet our team, we’re going to host an “office hour” session on Wednesday, October 26th at Noon US Eastern time in the voice channel over on our [discord server](https://discord.gg/PfR7a79FpQ). If you’d like to chat or ask any questions, please join us there. We’ll also be releasing another blog post in 1-2 months updating everyone on all the new changes coming.

We hope you’ll be a part of our journey.
