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
        
        # TODO: Initialize numpy arrays for storing data
        # self.observations = np.zeros((buffer_size, observation_dim))
        # self.actions = np.zeros((buffer_size, action_dim))
        # etc.
        
        self.pos = 0  # Current position in buffer
        
    def add(self, obs, action, reward, value, log_prob, done):
        """Add single transition to buffer."""
        # TODO: Store data at current position
        # Increment position
        pass
    
    def reset(self):
        """Clear buffer."""
        self.pos = 0
    
    def is_full(self) -> bool:
        """Check if buffer is full."""
        return self.pos >= self.buffer_size
