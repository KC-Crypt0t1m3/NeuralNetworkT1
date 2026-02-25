"""
Rollout Buffer for storing trajectories.
"""

import numpy as np


class RolloutBuffer:
    """
    Buffer for on-policy RL (PPO).
    Stores: observations, actions, rewards, values, log_probs, dones
    
    TODO: Implement buffer storage and retrieval
    - add(): Add single step to buffer
    - reset(): Clear buffer
    - get(): Return all stored data
    """
    
    def __init__(self, buffer_size: int, observation_dim: int, action_dim: int):
        self.buffer_size = buffer_size
        self.observation_dim = observation_dim
        self.action_dim = action_dim

        # Allocate memory
        self.observations = np.zeros((buffer_size, observation_dim), dtype=np.float32)
        self.actions      = np.zeros((buffer_size, action_dim), dtype=np.float32)
        self.rewards      = np.zeros(buffer_size, dtype=np.float32)
        self.values       = np.zeros(buffer_size, dtype=np.float32)
        self.log_probs    = np.zeros(buffer_size, dtype=np.float32)
        self.dones        = np.zeros(buffer_size, dtype=np.float32)

        self.pos = 0

    def add(self, obs, action, reward, value, log_prob, done):
        """Add single transition to buffer."""
        if self.pos >= self.buffer_size:
            raise IndexError("RolloutBuffer is full")

        self.observations[self.pos] = obs
        self.actions[self.pos] = action
        self.rewards[self.pos] = reward
        self.values[self.pos] = value
        self.log_probs[self.pos] = log_prob
        self.dones[self.pos] = done

        self.pos += 1

    def reset(self):
        """Clear buffer."""
        self.pos = 0

    def is_full(self) -> bool:
        """Check if buffer is full."""
        return self.pos >= self.buffer_size

    def get(self):
        """Return all stored data up to current position."""
        return {
            "observations": self.observations[:self.pos],
            "actions": self.actions[:self.pos],
            "rewards": self.rewards[:self.pos],
            "values": self.values[:self.pos],
            "log_probs": self.log_probs[:self.pos],
            "dones": self.dones[:self.pos],
        }
