"""
Actor-Critic Network
Resource: https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html#actor-critic

The Actor-Critic combines:
- Actor: Policy network (outputs actions)
- Critic: Value network (estimates V(s))
"""

import torch
import torch.nn as nn
from .lidar_encoder import LidarEncoder


class ActorCritic(nn.Module):
    """
    Actor-Critic with shared feature extractor.
    
    Architecture:
    1. Lidar Encoder: Process lidar data
    2. Combine with proprioceptive sensors (velocity, orientation)
    3. Actor head: Output action distribution (mean, std)
    4. Critic head: Output value estimate
    
    TODO: Implement the network architecture
    """
    
    def __init__(
        self,
        n_distance_sensors: int = 12,    # 12 distance sensors
        n_servo_positions: int = 12,     # 12 servo position readings
        n_imu: int = 6,                  # IMU: vel_x, vel_y, vel_z, roll, pitch, yaw
        action_dim: int = 12,            # 12 servo commands (4 legs * 3 servos)
    ):
        super(ActorCritic, self).__init__()
        
        # Total observation dimension
        self.obs_dim = n_distance_sensors + n_servo_positions + n_imu  # 30 total
        self.action_dim = action_dim
        
        # TODO: Initialize components
        # Option 1: Simple approach - use MLP on raw observations
        # self.shared_network = nn.Sequential(
        #     nn.Linear(self.obs_dim, 128),
        #     nn.ReLU(),
        #     nn.Linear(128, 64),
        #     nn.ReLU()
        # )
        
        # Option 2: Separate encoders for different sensor types
        # self.sensor_encoder = nn.Linear(n_distance_sensors, 32)
        # self.proprioceptive_encoder = nn.Linear(n_servo_positions + n_imu, 32)
        # Then combine: 32 + 32 = 64 features
        
        # 2. Actor network (policy)
        # - Input: encoded features
        # - Output: action mean (use tanh to bound to [-1, 1])
        # - Learn log_std as parameter
        
        # 3. Critic network (value function)
        # - Input: encoded features
        # - Output: single value estimate
        
    def forward(self, observation: torch.Tensor):
        """
        Forward pass.
        
        Args:
            observation: [batch, 30] = [12 distance sensors, 12 servo positions, 6 IMU]
        
        Returns:
            action_mean: [batch, 12]  - Commands for 12 servos
            value: [batch, 1]         - State value estimate
        """
        # TODO: Implement forward pass
        # 1. Option A - Simple: Pass entire observation through network
        #    features = self.shared_network(observation)
        
        # 2. Option B - Split and encode separately:
        #    distance_sensors = observation[:, :12]
        #    servo_positions = observation[:, 12:24]
        #    imu = observation[:, 24:30]
        #    
        #    sensor_features = self.sensor_encoder(distance_sensors)
        #    proprio_features = self.proprio_encoder(torch.cat([servo_positions, imu], dim=1))
        #    features = torch.cat([sensor_features, proprio_features], dim=1)
        
        # 3. Pass through actor and critic heads
        pass
    
    def get_action(self, observation: torch.Tensor, deterministic: bool = False):
        """
        Sample action from policy.
        
        TODO: Implement action sampling
        - Get action_mean from forward pass
        - Sample from Normal(mean, std) if not deterministic
        - Return action, log_prob, value
        
        Resource: torch.distributions.Normal
        """
        pass
    
    def evaluate_actions(self, observation: torch.Tensor, action: torch.Tensor):
        """
        Evaluate log_prob and entropy of given actions (for training).
        
        TODO: Implement action evaluation
        - Used during PPO update to compute policy loss
        """
        pass
