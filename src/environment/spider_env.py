"""
Spider-Bot Gymnasium Environment
Resource: https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/

Gym/Gymnasium provides a standard interface for RL environments.
"""

import gymnasium as gym
import numpy as np
from typing import Tuple, Dict


class SpiderBotEnv(gym.Env):
    """
    Custom environment for 4-legged spider-bot.
    
    Hardware:
    - 4 legs with 3 servos each = 12 servos total
    - 12 distance sensors (one per servo)
    - IMU for body orientation
    
    Observation space (30 dimensions):
    - 12 distance sensor readings [0, max_range]
    - 12 servo positions [0, 180 degrees]
    - 6 IMU readings (velocities + orientation)
    
    Action space (12 dimensions):
    - 12 servo commands [-1, 1] normalized
    
    TODO: Implement the Gym interface
    - __init__: Set up observation/action spaces
    - reset(): Reset environment, return initial observation
    - step(): Execute action, return (obs, reward, done, truncated, info)
    - _compute_reward(): Your reward function
    """
    
    def __init__(self, config: dict):
        super(SpiderBotEnv, self).__init__()
        
        # TODO: Define observation and action spaces
        # Observation: 12 sensors + 12 servo positions + 6 IMU = 30 total
        # self.observation_space = gym.spaces.Box(
        #     low=np.array([0]*12 + [0]*12 + [-np.inf]*6),  # Min values
        #     high=np.array([4.0]*12 + [180]*12 + [np.inf]*6),  # Max values
        #     dtype=np.float32
        # )
        
        # Action: 12 servo commands, normalized to [-1, 1]
        # self.action_space = gym.spaces.Box(
        #     low=-1.0,
        #     high=1.0,
        #     shape=(12,),
        #     dtype=np.float32
        # )
        
        # TODO: Initialize robot interface and sensor processor
        # self.robot = RobotInterface(config)
        # self.sensor_processor = LidarProcessor(config)  # Rename to SensorProcessor
        
    def reset(self, seed=None, options=None):
        """
        Reset environment to initial state.
        
        TODO: Implement reset
        - Reset robot to starting position
        - Get initial observation
        - Return (observation, info)
        """
        super().reset(seed=seed)
        # TODO: Implementation
        pass
    
    def step(self, action: np.ndarray) -> Tuple:
        """
        Execute action and return result.
        
        TODO: Implement step
        1. Send action to robot
        2. Read sensors (lidar, IMU, etc.)
        3. Compute reward
        4. Check if episode done
        5. Return (observation, reward, terminated, truncated, info)
        """
        # TODO: Implementation
        pass
    
    def _compute_reward(self) -> float:
        """
        Design your reward function here!
        
        Ideas:
        - Positive reward for forward movement
        - Penalty for collisions
        - Penalty for excessive tilt
        - Penalty for high energy usage
        - Reward for smooth motion
        
        TODO: Implement based on your objectives
        """
        reward = 0.0
        
        # Example components:
        # forward_reward = self.velocity[0] * 0.1
        # collision_penalty = -1.0 if self.collision else 0.0
        # stability_penalty = -abs(self.tilt) * 0.05
        
        return reward
    
    def close(self):
        """Clean up resources."""
        # TODO: Close robot interface
        pass
