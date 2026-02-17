"""
Deployment Script for Jetson Orin Nano
Run trained policy on hardware in real-time.

IMPORTANT: Test thoroughly in safe environment first!
"""

import torch


def deploy(model_path: str):
    """
    Deploy policy on Jetson.
    
    TODO: Implement deployment
    1. Load model (use TorchScript for speed)
    2. Set to eval mode
    3. Use FP16 for faster inference: model.half()
    4. Real-time control loop:
        - Read sensors
        - Get action (deterministic)
        - Send motor commands
        - Repeat at control frequency (e.g., 20 Hz)
    
    Jetson optimization tips:
    - Use torch.jit.script() or torch.jit.trace()
    - Enable CUDA if available
    - Consider TensorRT for max speed
    """
    
    print("Starting deployment on Jetson...")
    
    # TODO: Load and optimize model
    # model = torch.jit.load(model_path)
    # model = model.half()  # FP16
    # model.eval()
    
    # TODO: Control loop
    # while True:
    #     obs = read_sensors()
    #     action = model.get_action(obs, deterministic=True)
    #     send_commands(action)
    #     time.sleep(1/20)  # 20 Hz
    
    pass


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    args = parser.parse_args()
    
    deploy(args.model)
