---
layout: blog
short_title: "Announcing Shimmy 1.0.0"
subtitle: "API Conversion for External Reinforcement Learning Environments"
title: "Announcing Shimmy 1.0.0 - an API Conversion Tool For External Reinforcement Learning Environments"
date: "2023-04-25"
excerpt: "We are excited to announce Shimmy 1.0.0, an API compatibility tool for converting a wide range of single and multi-agent environments to the Gymnasium and PettingZoo APIs"
thumbnail: assets/posts/2023-04-25-Announcing-Shimmy/banner-gradient-line2.png
image: assets/posts/2023-04-25-Announcing-Shimmy/banner-gradient-line2.png
read_time: 3
---

Have you ever wanted to use [dm-control](https://github.com/deepmind/dm_control) with [stable-baselines3](https://github.com/DLR-RM/stable-baselines3)?
Within Reinforcement learning (RL), a number of API's are used to implement environments, with limited ability to convert between them. This makes training agents across different API's highly difficult, and has resulted in a fractured ecosystem. 

To address this issue, we are excited to announce [Shimmy](https://shimmy.farama.org/), an API compatibility tool for converting external RL environments to the [Gymnasium](https://gymnasium.farama.org/) and [PettingZoo](https://pettingzoo.farama.org/) APIs.
This allows users to access a wide range of single and multi-agent environments, all under a single standard API. 


<center>
    <a href="assets/posts/2023-04-25-Announcing-Shimmy/shimmy-demo.mp4">
        <video title="Shimmy demo" autoplay loop muted controls width="90%" src="assets/posts/2023-04-25-Announcing-Shimmy/shimmy-demo.mp4" type="video/mp4"></video>
    </a>
</center>

As detailed in our [announcement](https://farama.org/Announcing-The-Farama-Foundation) blog post, the Farama Foundation's greater goal is to create a unified and user-friendly ecosystem for open-source reinforcement learning software, for both research and industry. Shimmy plays an important role in this plan, by integrating popular external RL environments inside the Farama ecosystem.

We plan to maintain Shimmy for the long term and are welcome to new contributions to support more external APIs.

### Environments

Shimmy includes API compatibility wrappers for the following environments.

**Single-agent (Gymnasium wrappers):**
- [DeepMind Control](https://github.com/deepmind/dm_control)
- [DeepMind Lab](https://github.com/deepmind/lab)
- [DeepMind Behavior Suite](https://github.com/deepmind/bsuite)
- [OpenAI Gym](https://github.com/openai/gym) - [V21](https://github.com/openai/gym/releases/tag/v0.21.0) (before breaking API changes)
- [OpenAI Gym](https://github.com/openai/gym) - [V26](https://github.com/openai/gym/releases/tag/0.26.0) (after breaking API changes, final release)
- [Arcade Learning Environment](https://github.com/mgbellemare/Arcade-Learning-Environment)

**Multi-agent (PettingZoo wrappers):**
- [DeepMind Control: Soccer](https://github.com/deepmind/dm_control/blob/main/dm_control/locomotion/soccer/README.md)
- [OpenSpiel](https://github.com/deepmind/open_spiel)
- [Melting Pot](https://github.com/deepmind/meltingpot)

### Key Features
Shimmy’s [documentation](https://shimmy.farama.org/) contains an overview of each environment, as well as full usage scripts and installation instructions—allowing users to easily load and interact with environments without digging through source code. 

We include automated testing for each environment, to ensure that converted environments are fully functional and are held to the same standards as native [Gymnasium](https://gymnasium.farama.org/) and [PettingZoo](https://pettingzoo.farama.org/) environments.

Furthermore, Shimmy provides full installation scripts for external environments which are not available in distributed releases (via [PyPi](https://pypi.org/) or elsewhere), along with [Dockerfiles](https://shimmy.farama.org/content/getting_started/#docker) which can be used to install on any platform (e.g., [DeepMind Lab](https://github.com/deepmind/lab) does not support Windows or macOS).

For more information, see Shimmy 1.0.0 release notes. 

