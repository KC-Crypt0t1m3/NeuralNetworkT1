# Spider-Bot PPO Controller

PPO-based RL controller for a 4-legged autonomous spider-bot with 12 servos and 4 distance sensors, optimized for Jetson Orin Nano.

## Hardware
- **4 legs** with 3 servos each (12 servos total)
- **12 distance sensors** (one per servo)
- **1 IMU** for body orientation
- **Jetson Orin Nano** for inference

## Project Structure

```
spider-bot-ppo/
├── config/              # YAML configuration files
├── src/
│   ├── algorithms/      # PPO implementation
│   ├── models/          # Neural network architectures
│   ├── environment/     # Robot environment wrapper
│   └── utils/           # Helper utilities
├── scripts/             # Training and deployment scripts
└── tests/               # Unit tests
```

## Setup

```bash
pip install -r requirements.txt
```

## Quick Start

1. Configure your robot specs in `config/robot_config.yaml`
2. Adjust PPO hyperparameters in `config/ppo_config.yaml`
3. Implement hardware interface in `src/environment/robot_interface.py`
4. Train: `python scripts/train.py`
5. Deploy: `python scripts/deploy.py`

## Key Files
- `IMPLEMENTATION_GUIDE.md` - Step-by-step implementation order
- `ARCHITECTURE.md` - System architecture and design
- `HARDWARE_SETUP.md` - Your specific hardware configuration

## Resources

- **PPO Paper**: https://arxiv.org/abs/1707.06347
- **OpenAI Spinning Up PPO**: https://spinningup.openai.com/en/latest/algorithms/ppo.html
- **PyTorch RL Tutorial**: https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
- **Jetson Optimization Guide**: https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/
