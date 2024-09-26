import math

def reward_function(params):
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    progress = params['progress']
    steps = params['steps']
    steering_angle = abs(params['steering_angle'])
    closest_waypoints = params['closest_waypoints']
    is_left_of_center = params['is_left_of_center']
    heading = params['heading']
    is_crashed = params['is_crashed']
    is_offtrack = params['is_offtrack']

    reward = 1.0

    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        reward = 1e-3

    if not all_wheels_on_track or is_offtrack:
        reward = 1e-3

    SPEED_THRESHOLD = 1.5
    if speed < SPEED_THRESHOLD:
        reward += 0.5
    else:
        reward += 2.0

    if steps > 0:
        progress_reward = (progress / steps) * 100
        reward += min(progress_reward, 10)

    if steering_angle > 15:
        reward *= 0.8

    if is_crashed:
        reward = 1e-3

    waypoints = params['waypoints']
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]

    track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
    track_direction = math.degrees(track_direction)

    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    if not is_left_of_center:
        reward *= 0.9

    return float(reward)
