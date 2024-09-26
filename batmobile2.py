def reward_function(params):
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    progress = params['progress']
    steps = params['steps']
    steering_angle = abs(params['steering_angle'])  # Consider absolute steering angle

    SPEED_THRESHOLD = 1.5  # Increased speed threshold

    # Calculate markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to the center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.7  # Reduced penalty
    elif distance_from_center <= marker_3:
        reward = 0.3  # Reduced penalty
    else:
        reward = 1e-3  # likely crashed/close to off track

    # Check if all four wheels are on track
    if not all_wheels_on_track:
        reward = 1e-3  # Penalize if the car goes off track

    # Encourage higher speeds with more weight
    if speed < SPEED_THRESHOLD:
        reward += 0.5  # Encourage car to maintain a minimum speed
    else:
        reward += 2.0  # High reward if the car goes fast

    # Reward progress
    if steps > 0:
        reward += (progress / steps) * 100  # Reward based on progress

    # Penalize sharp turns
    if steering_angle > 15:  # Arbitrary angle threshold
        reward *= 0.8  # Penalize excessive steering

    return float(reward)
