#  after train the first model i change it and train it more to do to better
import math


def reward_function(params):
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']

    # Calculate 3 markers that are at varying distances from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Base reward
    reward = 1.0

    # Reward for distance from center
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed or close to off track

    # Penalize if the car goes off track
    if not all_wheels_on_track:
        reward = 1e-3

    # Reward for higher speeds
    reward += speed / 2

    # Calculate the direction of the center line based on the closest waypoints
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]

    # Calculate the direction in radians
    track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
    # Convert to degrees
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    return float(reward)
