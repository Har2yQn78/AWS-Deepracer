import math

def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    progress = params['progress']
    speed = params['speed']
    steering_angle = params['steering_angle']
    is_crashed = params['is_crashed']
    is_offtrack = params['is_offtrack']
    steps = params['steps']
    closest_waypoints = params['closest_waypoints']
    waypoints = params['waypoints']
    heading = params['heading']

    reward = 1.0

    if not all_wheels_on_track or is_crashed or is_offtrack:
        return 1e-3

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
        reward += 1e-3

    SPEED_THRESHOLD = 2.0
    if speed >= SPEED_THRESHOLD:
        reward += 0.5

    ABS_STEERING_THRESHOLD = 15.0
    if abs(steering_angle) > ABS_STEERING_THRESHOLD:
        reward *= 0.8


    reward += progress / 100.0

    next_waypoint = waypoints[closest_waypoints[1]]
    track_direction = math.atan2(next_waypoint[1] - params['y'], next_waypoint[0] - params['x'])
    track_direction = math.degrees(track_direction)
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    reward += (1 - (direction_diff / 180.0)) ** 2


    if steps > 0:
        reward += progress / steps

    return float(reward)
