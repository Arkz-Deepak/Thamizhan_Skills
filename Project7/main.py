import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

# ---------------------------------------------------------
# 1. THE PID CONTROLLER (The Brain)
# ---------------------------------------------------------
class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp  # Proportional (Speed)
        self.Ki = Ki  # Integral (Accumulated Error)
        self.Kd = Kd  # Derivative (Dampening/Smoothing)
        self.prev_error = 0
        self.integral = 0

    def compute(self, target, current, dt):
        error = target - current
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        
        # The PID Formula
        output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
        return output

# ---------------------------------------------------------
# 2. THE DRONE PHYSICS SIMULATOR
# ---------------------------------------------------------
def simulate_flight(waypoints):
    # Setup PID controllers for X, Y, Z axes
    # (Tuned values for smooth flight)
    pid_x = PID(1.0, 0.0, 1.5)
    pid_y = PID(1.0, 0.0, 1.5)
    pid_z = PID(1.5, 0.05, 2.5) # Z needs more power to fight gravity

    # Initial Position
    x, y, z = 0, 0, 0
    dt = 0.1 # Time step
    
    # For plotting history
    history_x, history_y, history_z = [], [], []

    print("🚁 DRONE TAKEOFF INITIATED...")
    
    for target in waypoints:
        print(f"   Flying to Waypoint: {target}")
        
        # Simulate 100 time steps per waypoint to get there smoothly
        for _ in range(60): 
            # Calculate Thrust needed to get to target
            thrust_x = pid_x.compute(target[0], x, dt)
            thrust_y = pid_y.compute(target[1], y, dt)
            thrust_z = pid_z.compute(target[2], z, dt)

            # Apply Physics (Simple Velocity update)
            x += thrust_x * dt
            y += thrust_y * dt
            z += thrust_z * dt

            history_x.append(x)
            history_y.append(y)
            history_z.append(z)

    return history_x, history_y, history_z

# ---------------------------------------------------------
# 3. RUN SIMULATION & PLOT
# ---------------------------------------------------------
# Define Waypoints (X, Y, Altitude)
# 1. Takeoff (0,0,10) -> 2. Move Right (10,0,10) -> 3. Move Forward (10,10,10) -> 4. Land (10,10,0)
mission_waypoints = [
    (0, 0, 0),    # Start
    (0, 0, 10),   # Takeoff
    (10, 0, 10),  # Move Right
    (10, 10, 10), # Move Forward
    (10, 10, 0)   # Land
]

hx, hy, hz = simulate_flight(mission_waypoints)

# 4. 3D VISUALIZATION
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the flight path
ax.plot(hx, hy, hz, label='Drone Flight Path', color='blue', linewidth=2)

# Plot the Waypoints
wx = [w[0] for w in mission_waypoints]
wy = [w[1] for w in mission_waypoints]
wz = [w[2] for w in mission_waypoints]
ax.scatter(wx, wy, wz, color='red', s=50, label='Waypoints')

# Draw "Ground"
ax.plot([0, 15], [0, 0], [0, 0], 'k--', alpha=0.3)
ax.plot([0, 0], [0, 15], [0, 0], 'k--', alpha=0.3)

ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Altitude (Z)')
ax.set_title('Autonomous Drone PID Flight Simulation')
ax.legend()

print("✅ Mission Complete. Displaying Flight Log.")
plt.show()