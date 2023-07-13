inches_per_step = 18*2
bpm = 60

# Convert inches to meters
distance_in_meters = inches_per_step * 0.0254

# Convert steps per minute to steps per second
total_distance_per_minute = distance_in_meters*bpm

# Calculate velocity in m/s
velocity = total_distance_per_minute / 60

print(f"Velocity: {velocity} m/s")