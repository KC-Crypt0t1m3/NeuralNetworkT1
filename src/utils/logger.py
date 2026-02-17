"""
Training Logger
Logs metrics to console and TensorBoard.

Resource: https://pytorch.org/docs/stable/tensorboard.html
"""

from torch.utils.tensorboard import SummaryWriter


class Logger:
    """
    Logger for training metrics.
    
    TODO: Implement logging
    - log_scalar(): Log single value
    - log_episode(): Log episode statistics
    - Save to TensorBoard
    """
    
    def __init__(self, log_dir: str = "logs/"):
        self.writer = SummaryWriter(log_dir)
        self.step = 0
    
    def log_scalar(self, tag: str, value: float, step: int = None):
        """Log a scalar value."""
        # TODO: Write to tensorboard
        pass
    
    def log_episode(self, episode_reward: float, episode_length: int):
        """Log episode statistics."""
        # TODO: Log episode metrics
        pass
    
    def close(self):
        """Close logger."""
        self.writer.close()
