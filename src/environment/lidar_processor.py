"""
Lidar Data Processing
Process raw lidar scans for use in RL.
"""

import numpy as np


class LidarProcessor:
    """
    Process and filter lidar data.
    
    TODO: Implement processing pipeline
    - Clip to valid range
    - Filter noise (median filter, etc.)
    - Downsample for faster processing
    - Normalize to [0, 1]
    
    Resource: scipy.signal.medfilt for noise filtering
    """
    
    def __init__(
        self,
        n_points: int = 360,
        min_range: float = 0.15,
        max_range: float = 12.0,
        downsample_factor: int = 4
    ):
        self.n_points = n_points
        self.min_range = min_range
        self.max_range = max_range
        self.downsample_factor = downsample_factor
        
    def process(self, raw_scan: np.ndarray) -> np.ndarray:
        """
        Process raw lidar scan.
        
        Args:
            raw_scan: Raw distances [n_points]
        
        Returns:
            Processed scan [n_points // downsample_factor]
        """
        # TODO: Implement processing
        # 1. Clip to valid range
        # 2. Replace inf/nan with max_range
        # 3. Apply median filter if desired
        # 4. Downsample
        # 5. Normalize to [0, 1]
        
        pass
