# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     TRAINING PHASE                           │
│                                                               │
│  ┌──────────────┐         ┌─────────────────┐               │
│  │ Spider-Bot   │ ◄────── │ PPO Algorithm   │               │
│  │ Environment  │         │                 │               │
│  │              │ ──────► │ - Collect data  │               │
│  │ - Sensors    │  obs    │ - Compute GAE   │               │
│  │ - Motors     │  reward │ - Update policy │               │
│  │ - Physics    │  done   │                 │               │
│  └──────────────┘         └─────────────────┘               │
│         │                          │                          │
│         │                          ▼                          │
│         │                 ┌─────────────────┐                │
│         │                 │  Actor-Critic   │                │
│         │                 │   Network       │                │
│         │                 │                 │                │
│         └────────────────►│ - Lidar Encoder │                │
│               lidar       │ - Actor Head    │                │
│                           │ - Critic Head   │                │
│                           └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT PHASE                          │
│                                                               │
│  ┌──────────────┐         ┌─────────────────┐               │
│  │ Real Robot   │         │ Trained Policy  │               │
│  │              │ ──────► │ (TorchScript)   │               │
│  │ - Lidar      │  sensors│                 │               │
│  │ - IMU        │         │ - Inference     │               │
│  │ - Motors     │ ◄────── │ - FP16 optimized│               │
│  │              │  actions│                 │               │
│  └──────────────┘         └─────────────────┘               │
│      Jetson Orin Nano                                        │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### During Training

1. **Environment Observation**
   ```
   12 Distance Sensors + 12 Servo Positions + 6 IMU values
        ↓
   Process & Normalize
        ↓
   Observation Vector [30 dimensions]
   ```

2. **Neural Network Forward Pass**
   ```
   Observation [30] = [12 sensors | 12 servos | 6 IMU]
        ↓
   ┌─────────────────────────────────────┐
   │ Option 1: Direct MLP                │
   │ [30] → [128] → [64]                 │
   └─────────────────────────────────────┘
        OR
   ┌─────────────────────────────────────┐
   │ Option 2: Separate Encoders         │
   │ Sensors[12] → [32]                  │
   │ Proprio[18] → [32]                  │
   │ Concat → [64]                       │
   └─────────────────────────────────────┘
        ↓
   Shared Features [64]
        ↓
        ├─────────────────┬────────────────┐
        ↓                 ↓                ↓
   ┌─────────┐    ┌──────────┐    ┌──────────┐
   │  Actor  │    │  Critic  │    │          │
   │ [64→128]│    │ [64→128] │    │          │
   │ [128→12]│    │ [128→1]  │    │          │
   └─────────┘    └──────────┘    │          │
        ↓              ↓            │          │
   Action Mean    Value Est.       │          │
   [12 servos]    [1 scalar]       │          │
        ↓                           │          │
   Sample Action                    │          │
   (with log_std)                   │          │
   ```

3. **Environment Step**
   ```
   Action [12] → Robot (12 servos) → New State
                          ↓
                        Reward
                          ↓
                    Store in Buffer
   ```

4. **PPO Update** (when buffer full)
   ```
   Buffer → Compute GAE → Advantages
                           ↓
                    Multiple Epochs
                           ↓
              ┌────────────┴──────────┐
              ↓                       ↓
       Policy Loss              Value Loss
    (clipped objective)      (MSE with returns)
              ↓                       ↓
              └────────────┬──────────┘
                           ↓
                    Total Loss + Entropy
                           ↓
                     Backpropagation
                           ↓
                    Update Weights
   ```

## Key Components

### 1. Sensor Encoder
**Purpose**: Process 12 distance sensor readings

**Input**: 12 distance values [n_sensors]
**Output**: Feature vector [feature_dim]

**Recommendation**: Simple MLP (12 sensors don't need CNN)
- Much simpler than processing 360-point LiDAR scans!
- Fast inference on Jetson

### 2. Actor Network
**Purpose**: Learn policy (action distribution)

**Input**: Combined features [lidar + proprioceptive]
**Output**: 
- Action mean [action_dim]
- Log std (learned parameter)

**Distribution**: Gaussian (continuous actions)

### 3. Critic Network
**Purpose**: Learn value function V(s)

**Input**: Combined features
**Output**: Value estimate (scalar)

**Used for**: Computing advantages (how much better is action than average)

### 4. PPO Algorithm

**Core Idea**: Trust region optimization with clipped objective

**Key equation**:
```
L_CLIP = E[min(r(θ) * A, clip(r(θ), 1-ε, 1+ε) * A)]

where:
- r(θ) = π_new(a|s) / π_old(a|s)  (probability ratio)
- A = advantage estimate
- ε = clip_epsilon (typically 0.2)
```

**Why it works**: Prevents too large policy updates (more stable training)

### 5. GAE (Generalized Advantage Estimation)

**Purpose**: Better advantage estimates using TD(λ)

**Key equation**:
```
A_t = Σ(γλ)^i * δ_{t+i}

where:
- δ_t = r_t + γV(s_{t+1}) - V(s_t)  (TD error)
- γ = discount factor
- λ = GAE lambda (trades off bias vs variance)
```

## Hardware Considerations

### Jetson Orin Nano Specs
- GPU: 1024-core NVIDIA Ampere
- RAM: 8GB
- Power: 7-15W

### Optimization Strategy
1. **Training**: Use workstation/cloud (faster)
2. **Inference**: Deploy to Jetson (edge computing)

### Deployment Optimizations
- **TorchScript**: Removes Python overhead
- **FP16**: Half precision (2x faster, ~same accuracy)
- **TensorRT**: Maximum optimization (optional, complex)
- **Batch size 1**: Real-time control

### Expected Performance
- Inference time target: <10ms (for 20Hz control)
- Model size: ~5-10MB (fits easily in memory)

## Observation Space Design

```python
Observation = [
    # Distance Sensors (12 individual readings)
    sensor[0],     # Distance from sensor 0 (e.g., leg 1, servo 1)
    sensor[1],     # Distance from sensor 1 (e.g., leg 1, servo 2)
    sensor[2],     # Distance from sensor 2 (e.g., leg 1, servo 3)
    ...
    sensor[11],    # Distance from sensor 11 (e.g., leg 4, servo 3)
    
    # Servo Positions (12 values)
    servo_pos[0],  # Current angle of servo 0 [0-180°]
    servo_pos[1],  # Current angle of servo 1
    ...
    servo_pos[11], # Current angle of servo 11
    
    # IMU - Proprioceptive sensors (6 values)
    vel_x,         # Forward velocity
    vel_y,         # Lateral velocity
    vel_z,         # Vertical velocity
    roll,          # Body roll angle
    pitch,         # Body pitch angle
    yaw_rate       # Rotation rate
]

Total: 30 dimensions (12 + 12 + 6)
```

## Action Space Design

```python
Action = [
    # Leg 1 (3 servos)
    leg1_servo1,   # Hip/Coxa
    leg1_servo2,   # Knee/Femur
    leg1_servo3,   # Ankle/Tibia
    
    # Leg 2 (3 servos)
    leg2_servo1,
    leg2_servo2,
    leg2_servo3,
    
    # Leg 3 (3 servos)
    leg3_servo1,
    leg3_servo2,
    leg3_servo3,
    
    # Leg 4 (3 servos)
    leg4_servo1,
    leg4_servo2,
    leg4_servo3,
]

Total: 12 dimensions (4 legs × 3 servos)
Range: [-1, 1] normalized (maps to [0, 180°] servo angles)
```

## Reward Function Design

Critical for success! Start simple, iterate.

```python
# Example reward function
reward = 0

# Primary objective: move forward
reward += velocity_forward * 0.1

# Safety: avoid collisions
if min(lidar_scan) < threshold:
    reward -= 10.0

# Stability: stay upright
reward -= abs(roll) * 0.5
reward -= abs(pitch) * 0.5

# Energy efficiency (optional)
reward -= action_magnitude * 0.01

# Living penalty (encourage finishing quickly)
reward -= 0.01

return reward
```

## File Dependencies

```
train.py
  ├─ spider_env.py
  │   ├─ robot_interface.py
  │   └─ lidar_processor.py
  ├─ actor_critic.py
  │   └─ lidar_encoder.py
  ├─ ppo.py
  │   └─ replay_buffer.py
  └─ logger.py

deploy.py
  ├─ actor_critic.py (TorchScript)
  └─ robot_interface.py
```

## Training Timeline

Rough estimates (varies greatly):

1. **Initial setup**: 1-2 weeks
   - Hardware interface
   - Basic environment
   - Network architecture

2. **First successful training**: 1-2 weeks
   - Debug training loop
   - Tune hyperparameters
   - Iterate on rewards

3. **Good performance**: 2-4 weeks
   - Refine reward function
   - Improve network architecture
   - Add curriculum learning

4. **Deployment & testing**: 1-2 weeks
   - Optimize for Jetson
   - Real robot testing
   - Safety validation

**Total**: 1.5-3 months for complete project

Remember: RL can be finicky. Success often comes from many small iterations!
