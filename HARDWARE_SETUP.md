# Hardware Setup Reference

## Your Spider-Bot Configuration

### Physical Setup
- **Legs**: 4
- **Servos per leg**: 3
- **Total servos**: 12
- **Distance sensors**: 12 (one per servo)
- **IMU**: 1 (for body orientation and velocity)

### Servo Layout
```
        Front
    Leg1      Leg2
     ╱ ╲      ╱ ╲
    S1 S2    S4 S5
     S3        S6
    
    Leg3      Leg4
     ╱ ╲      ╱ ╲
    S7 S8   S10 S11
     S9       S12
        Back

S1-S12 = Servos 1-12
Each servo has an associated distance sensor
```

### Neural Network I/O

#### Inputs (Observations) - 30 dimensions
```
┌─────────────────────────────────────────┐
│ Distance Sensors (12)                   │
├─────────────────────────────────────────┤
│ sensor_0  : distance from servo 1 sensor│
│ sensor_1  : distance from servo 2 sensor│
│ ...                                     │
│ sensor_11 : distance from servo 12 sensor│
├─────────────────────────────────────────┤
│ Servo Positions (12)                    │
├─────────────────────────────────────────┤
│ servo_0   : current angle of servo 1    │
│ servo_1   : current angle of servo 2    │
│ ...                                     │
│ servo_11  : current angle of servo 12   │
├─────────────────────────────────────────┤
│ IMU (6)                                 │
├─────────────────────────────────────────┤
│ vel_x     : forward velocity            │
│ vel_y     : lateral velocity            │
│ vel_z     : vertical velocity           │
│ roll      : body roll angle             │
│ pitch     : body pitch angle            │
│ yaw_rate  : rotation rate               │
└─────────────────────────────────────────┘
```

#### Outputs (Actions) - 12 dimensions
```
┌─────────────────────────────────────────┐
│ Servo Commands (12)                     │
├─────────────────────────────────────────┤
│ command_0  : target for servo 1 [-1,1]  │
│ command_1  : target for servo 2 [-1,1]  │
│ ...                                     │
│ command_11 : target for servo 12 [-1,1] │
└─────────────────────────────────────────┘

Note: [-1, 1] gets mapped to [0°, 180°]
```

## Network Architecture Recommendation

For your simpler setup (30 inputs, 12 outputs), use a straightforward architecture:

```python
Input [30]
   ↓
Linear(30 → 128) + ReLU
   ↓
Linear(128 → 64) + ReLU
   ↓
   ├────────────┬──────────┐
   ↓            ↓          ↓
Actor         Critic    (shared)
Linear(64→128) Linear(64→128)
Linear(128→12) Linear(128→1)
   ↓            ↓
Action[12]   Value[1]
```

**Why this is simpler than typical setups:**
- No need for CNN (only 12 sensors, not 360-point scans)
- Smaller network = faster on Jetson
- Less overfitting risk with limited sensors

## Sensor Notes

### Distance Sensors
If each servo has a LiDAR sensor, you likely have:
- **Option A**: 12 individual distance sensors (e.g., VL53L0X time-of-flight)
- **Option B**: 12 small scanning LiDARs (unlikely, expensive)
- **Option C**: 12 ultrasonic/IR sensors

Most likely **Option A** - single distance reading per sensor.

### Typical Ranges
- **Time-of-Flight (LiDAR)**: 2cm - 4m, very accurate
- **Ultrasonic**: 2cm - 4m, less accurate, affected by surface
- **IR Sharp sensor**: 10cm - 80cm, nonlinear response

Adjust `min_range` and `max_range` in `config/robot_config.yaml` accordingly!

## Communication Protocol Ideas

### Servo Control
Most common setups:
1. **PWM Servo Controller** (e.g., PCA9685)
   - I2C interface
   - Controls up to 16 servos
   - Python: `smbus2` library
   
2. **Serial Servo Controller** (e.g., Pololu Maestro)
   - USB/Serial interface
   - Python: `pyserial` library
   
3. **Arduino as middleman**
   - Jetson → (Serial) → Arduino → (PWM) → Servos
   - Arduino handles real-time PWM
   - Jetson sends high-level commands

### Sensor Reading
- **I2C sensors**: Can often chain multiple on same bus
- **Analog sensors**: Need ADC (Arduino or I2C ADC chip)
- **Digital sensors**: SPI or I2C

## Example Message Format (Serial)

If using serial communication to servo controller:

```python
# Command format (one approach):
# [START_BYTE][SERVO_ID][ANGLE_HIGH][ANGLE_LOW][CHECKSUM][END_BYTE]

def send_servo_command(servo_id, angle):
    msg = bytearray()
    msg.append(0xFF)              # Start byte
    msg.append(servo_id)          # Servo ID (0-11)
    msg.append((angle >> 8) & 0xFF)  # High byte of angle
    msg.append(angle & 0xFF)      # Low byte of angle
    checksum = (servo_id + angle) % 256
    msg.append(checksum)
    msg.append(0xFE)              # End byte
    serial_port.write(msg)
```

## Recommended Implementation Order

1. **Test servo control manually**
   - Send static commands to each servo
   - Verify full range of motion
   - Check for mechanical collisions!

2. **Test sensor reading**
   - Read all 12 sensors
   - Verify readings make sense
   - Check update rate (should be >10Hz)

3. **Test IMU**
   - Read orientation and velocity
   - Verify axes are correct
   - Calibrate if needed

4. **Integrate into RobotInterface**
   - Combine servo + sensor + IMU
   - Test in environment wrapper

5. **Train with RL**
   - Start with simple reward (move forward)
   - Iterate based on behavior

## Safety Considerations

1. **Emergency stop**: Button or command that stops all servos
2. **Soft start**: Gradually move to target positions (not instant jumps)
3. **Limit checks**: Prevent positions that cause collisions
4. **Timeout**: If no command for X seconds, enter safe mode
5. **Power**: Ensure adequate power supply (12 servos draw significant current!)

## Wiring Tips

- **Power servos separately** from Jetson (they draw lots of current)
- **Common ground** between Jetson and servo power supply
- **Pull-up resistors** for I2C (typically 4.7kΩ)
- **Decoupling capacitors** near servo power inputs
- **Keep sensor wiring short** to reduce noise

## Testing Without Hardware

Use mock mode in `robot_interface.py`:
```python
robot = RobotInterface({"interface": "mock"})
```

This lets you:
- Test RL algorithm
- Debug training loop
- Develop reward functions
- All without risk to hardware!

Once training works in simulation/mock, deploy to real robot.
