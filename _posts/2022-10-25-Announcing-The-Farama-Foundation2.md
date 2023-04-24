---
layout: blog
short_title: "Announcing The Farama Foundation2"
subtitle: "The future of open source reinforcement learning"
title: "Announcing The Farama Foundation2 - The future of open source reinforcement learning"
date: "2022-10-25"
excerpt: "Today we're announcing the Farama Foundation – a new nonprofit organization designed in part to house major existing open source reinforcement learning (“RL”) libraries in a neutral nonprofit body."
thumbnail: assets/posts/2022-10-25-Announcing-The-Farama-Foundation/banner-gradient-proto-lines3.png
image: assets/posts/2022-10-25-Announcing-The-Farama-Foundation/banner-gradient-proto-lines3.png
read_time: 12
---

## Announcing Shimmy
Lack of compatibility between environments, training libraries and API's is a major problem in reinforcement learning
A major problem in reinforcement learning research is a lack of compatibility between environments, training libraries and API’s. 
This results in a fractured ecosystem, and many single-problem solutions that cannot be easily adapted to new domains. 
Have you ever wanted to use [dm-control](https://github.com/deepmind/dm_control) with [stable-baselines-3](https://github.com/DLR-RM/stable-baselines3), or train other non-gymnasium based environments with standard learning libraries? 

We are excited to announce Shimmy, an API compatibility tool for converting a wide range of single and multi-agent environments to the [Gymnasium](https://gymnasium.farama.org/) and [PettingZoo](https://pettingzoo.farama.org/) APIs.
This allows users to conduct experiments across many external environments, all under a single standard API. 

video

As detailed in our [Announcing The Farama Foundation](https://farama.org/Announcing-The-Farama-Foundation) blog post, our greater goal at Farama is to create a unified and user-friendly ecosystem for open-source reinforcement learning software, for use both in research and in industry. Shimmy plays an important role in this plan, by integrating external RL environments inside of the Farama ecosystem.
Shimmy will continue to be maintained as a longer-term compatibility tool, ensuring that popular RL environments are compatible with up-to-date APIs. We plan to add other external environments as we see fit, and welcome new contributions or suggestions.

## Overview

Shimmy includes API compatibility for the following environments: 
### Single-agent (Gymnasium wrappers)
- Arcade Learning Environments 
- DeepMind Control
- DeepMind Lab
- DeepMind Behavior Suite
- OpenAI Gym - V21 (before breaking API changes)
- OpenAI Gym - V26 (after breaking API changes, final release)

### Multi-agent (PettingZoo wrappers)
- DeepMind OpenSpiel
- DeepMind Control: Soccer
- DeepMind Melting Pot

## Key Features
Shimmy’s documentation contains an overview of each environment, as well as full usage scripts and installation instructions--allowing users to easily load and interact with environments without digging through source code. 

We additionally include automated testing for each environment, ensuring their converted environments are fully functional and held to the same standards as native Gymnasium or PettingZoo environments. 
This includes API tests, random seeding tests (for deterministic environments), rendering tests, and tests ensuring each environment can be serialized/deserialized via pickle. 

Shimmy also provides full installation scripts for external environments which are not available in distributed releases (via PyPi or elsewhere), and Dockerfiles which can be used to install on any platform (e.g., DeepMind Lab does not support macOS or Windows). 

For more information, see Shimmy 1.0.0 release notes. 
