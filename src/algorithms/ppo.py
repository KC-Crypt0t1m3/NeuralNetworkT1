"""
PPO Algorithm Implementation
Resource: https://arxiv.org/abs/1707.06347
Spinning Up Guide: https://spinningup.openai.com/en/latest/algorithms/ppo.html
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, Tuple


class PPO:
    """
    Proximal Policy Optimization with clipped objective.
    
    Key components to implement:
    1. Compute GAE (Generalized Advantage Estimation)
    2. PPO clipped surrogate loss
    3. Value function loss
    4. Entropy bonus for exploration
    5. Multiple epochs of minibatch updates
    """
    
    def __init__(
        self,
        actor_critic: nn.Module,
        learning_rate: float = 3e-4,
        gamma: float = 0.99,
        gae_lambda: float = 0.95,
        clip_epsilon: float = 0.2,
        value_loss_coef: float = 0.5,
        entropy_coef: float = 0.01,
        device: str = "cpu"
    ):
        self.actor_critic = actor_critic.to(device)
        self.device = device
        
        # TODO: Store hyperparameters
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.clip_epsilon = clip_epsilon
        # ... store other hyperparameters
        
        # TODO: Initialize optimizer (Adam is standard)
        # self.optimizer = torch.optim.Adam(...)
        
    def compute_gae(self, rewards, values, dones, next_value) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute Generalized Advantage Estimation.
        
        TODO: Implement GAE calculation
        - Loop backwards through trajectory
        - Calculate TD error: delta = r + gamma * V(s') - V(s)
        - Accumulate advantages with gae_lambda
        
        Resource: https://arxiv.org/abs/1506.02438
        
        Returns:
            advantages: Advantage estimates
            returns: Discounted returns (advantages + values)
        """
        # TODO: Implement GAE
        pass
    
    def update(self, rollout_buffer) -> Dict[str, float]:
        """
        Update policy using collected rollouts.
        
        TODO: Implement PPO update
        1. Compute advantages using GAE
        2. Normalize advantages
        3. For n_epochs:
            - Create minibatches
            - Calculate policy loss (clipped objective)
            - Calculate value loss
            - Calculate entropy
            - Backpropagate and update
        
        Returns:
            Dictionary of loss metrics
        """
        # TODO: Implement update logic
        pass
    
    def save(self, path: str):
        """Save model checkpoint."""
        # TODO: Save actor_critic and optimizer state
        pass
    
    def load(self, path: str):
        """Load model checkpoint."""
        # TODO: Load saved states
        pass
