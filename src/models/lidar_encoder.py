"""
Sensor Encoder Network
Processes distance sensor readings into feature vectors.

For your setup: 12 individual distance sensors (not scanning LiDARs)
This is simpler than processing 360-point scans!

Approach options:
1. Simple MLP: Best for 12 individual readings
2. 1D CNN: If sensors have spatial relationship (e.g., arranged in order around body)

Resource: https://pytorch.org/docs/stable/nn.html
"""

import torch
import torch.nn as nn


class SensorEncoder(nn.Module):
    """
    Encode distance sensor readings into feature vector.
    
    For 12 individual distance sensors (one per servo).
    Much simpler than full LiDAR processing!
    
    TODO: Choose and implement architecture
    - Option 1: Simple MLP (recommended for 12 sensors)
    - Option 2: 1D Conv if sensors have spatial ordering
    
    Input: [batch_size, 12]  - 12 distance readings
    Output: [batch_size, feature_dim]
    """
    
    def __init__(self, n_sensors: int = 12, feature_dim: int = 32):
        super(SensorEncoder, self).__init__()
        
        self.n_sensors = n_sensors
        self.output_dim = feature_dim
        
        # TODO: Define your network layers
        # Simple MLP example:
        # self.network = nn.Sequential(
        #     nn.Linear(n_sensors, 64),
        #     nn.ReLU(),
        #     nn.Linear(64, feature_dim),
        #     nn.ReLU()
        # )
        
    def forward(self, sensor_readings: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        
        Args:
            sensor_readings: [batch_size, 12] - Distance readings from 12 sensors
        Returns:
            features: [batch_size, feature_dim]
        """
        # TODO: Implement forward pass
        # return self.network(sensor_readings)
        pass


class LidarEncoder(nn.Module):
    """
    LEGACY: For scanning LiDAR (360+ points).
    
    Your bot uses 12 individual sensors, so use SensorEncoder instead!
    Keeping this for reference if you upgrade to scanning LiDAR later.
    """
    
    def __init__(self, n_points: int = 360, feature_dim: int = 64):
        super(LidarEncoder, self).__init__()
        
        self.n_points = n_points
        self.output_dim = feature_dim
        
        # 1D CNN for spatial patterns in scan
        # TODO: Implement if using scanning LiDAR
        
    def forward(self, lidar_scan: torch.Tensor) -> torch.Tensor:
        """Process full 360-point LiDAR scan."""
        pass
