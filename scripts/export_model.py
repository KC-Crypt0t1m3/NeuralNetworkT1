"""
Export Model for Deployment
Convert PyTorch model to optimized format (TorchScript/ONNX).

Resource: https://pytorch.org/tutorials/beginner/Intro_to_TorchScript_tutorial.html
"""

import torch


def export_to_torchscript(checkpoint_path: str, output_path: str):
    """
    Export to TorchScript for Jetson deployment.
    
    TODO: Implement export
    - Load checkpoint
    - Use torch.jit.trace() or torch.jit.script()
    - Save traced model
    """
    
    print(f"Exporting {checkpoint_path} to {output_path}")
    
    # TODO: Load model
    # model = ActorCritic(...)
    # model.load_state_dict(checkpoint)
    # model.eval()
    
    # TODO: Trace model
    # example_input = torch.randn(1, observation_dim)
    # traced_model = torch.jit.trace(model, example_input)
    # traced_model.save(output_path)
    
    pass


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--output", type=str, default="checkpoints/model_traced.pt")
    args = parser.parse_args()
    
    export_to_torchscript(args.checkpoint, args.output)
