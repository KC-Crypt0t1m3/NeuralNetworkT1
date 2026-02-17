"""
Robot Hardware Interface
This is where you'll interface with your actual hardware.

Depends on your setup:
- Serial communication (pyserial)
- I2C (smbus2)
- ROS2 (rclpy)
- Direct GPIO (if using Jetson pins)
"""

import numpy as np


class RobotInterface:
    """
    Interface for spider-bot hardware.
    
    TODO: Implement based on your hardware setup
    - __init__: Connect to robot
    - send_motor_commands(): Send PWM/angle commands
    - read_sensors(): Get motor positions, IMU data
    - read_lidar(): Get lidar scan
    - emergency_stop(): Safety mechanism
    """
    
    def __init__(self, config: dict):
        """
        Initialize hardware connection.
        
        TODO: Set up communication
        - Serial: import serial; serial.Serial(port, baudrate)
        - I2C: import smbus2; smbus2.SMBus(bus_number)
        - ROS: import rclpy; rclpy.init()
        """
        self.interface_type = config.get("interface", "serial")
        
        # Your hardware: 4 legs, 3 servos per leg = 12 servos
        self.n_legs = config.get("n_legs", 4)
        self.servos_per_leg = config.get("servos_per_leg", 3)
        self.n_servos = self.n_legs * self.servos_per_leg  # 12 total
        self.n_sensors = config.get("n_sensors", 12)  # 12 distance sensors
        
        # TODO: Initialize your connection
        
    def send_motor_commands(self, actions: np.ndarray) -> bool:
        """
        Send motor commands to all 12 servos.
        
        Args:
            actions: Normalized commands [-1, 1] for each of 12 servos
                    [leg1_servo1, leg1_servo2, leg1_servo3,
                     leg2_servo1, leg2_servo2, leg2_servo3,
                     leg3_servo1, leg3_servo2, leg3_servo3,
                     leg4_servo1, leg4_servo2, leg4_servo3]
        
        TODO: Implement communication protocol
        - Convert normalized actions [-1,1] to servo angles [0, 180]
        - Format message for your servo controller
        - Send via serial/I2C/ROS
        
        Example conversion:
        servo_angles = (actions + 1.0) * 90.0  # Maps [-1,1] to [0,180]
        """
        pass
    
    def read_sensors(self) -> dict:
        """
        Read all sensors.
        
        Returns:
            Dictionary with sensor readings:
            - distance_sensors: [12] distances from sensors
            - servo_positions: [12] current servo angles
            - servo_velocities: [12] servo angular velocities (optional)
            - imu_orientation: [3] roll, pitch, yaw
            - imu_velocity: [3] vel_x, vel_y, vel_z
        
        TODO: Implement sensor reading
        """
        pass
    
    def read_distance_sensors(self) -> np.ndarray:
        """
        Read 12 distance sensors (one per servo).
        
        TODO: Implement based on your sensor type
        - If LiDAR sensors: Read distance value from each
        - If ultrasonic: Trigger and read each sensor
        - If IR: Read analog values and convert to distance
        
        Returns:
            distances: Array of 12 distance readings [meters]
        """
        pass
    
    def emergency_stop(self):
        """
        Emergency stop all motors.
        IMPORTANT: Implement this for safety!
        """
        pass
    
    def close(self):
        """Clean up connections."""
        pass
