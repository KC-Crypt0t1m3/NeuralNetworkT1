"""
Testing Script
Evaluate trained policy.

Usage: python scripts/test.py --checkpoint checkpoints/best_model.pth
"""

import torch
import argparse


def test(checkpoint_path: str, n_episodes: int = 10):
    """
    Test trained policy.
    
    TODO: Implement testing
    1. Load trained model
    2. Create environment
    3. Run episodes with deterministic actions
    4. Log performance metrics
    """
    
    # TODO: Load model and run evaluation
    
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--n_episodes", type=int, default=10)
    args = parser.parse_args()
    
    test(args.checkpoint, args.n_episodes)
