import pandas as pd
import numpy as np
from .preprocessing import preprocess_vehicle_data, calculate_mean_of_last_frames, calculate_mean_of_first_frames, flatten_list_of_arrays, filter_float_in_series_of_lists
from .lane_changing import detect_lane_changes
from tqdm import tqdm

def detect_entering_vehicles(data, interaction_distance_threshold=50, relative_speed_threshold=0.5, tailgating_distance_threshold=5, yielding_speed_threshold=1, yielding_distance_threshold=5, check_hard_braking=True):
    """
    Detect vehicles that are exhibiting entering or merging behavior based on certain conditions.
    :param data: DataFrame containing the dataset.
    :return: A DataFrame with entering vehicles marked.
    """

    # Define thresholds for entering behavior
    speed_increase_threshold = 0.5  # Adjust based on your specific criteria
    initial_frames_threshold = 5  # Check the first 5 frames for each vehicle
    lane_change_threshold = 0.9  # Threshold for considering lane change towards entry

    ############################# Preprocessing ################################

    data = preprocess_vehicle_data(data)

    ############################################################################

    # Create a new column to identify entering vehicles

    detect_lane_changes(data)

    data['is_entering'] = False
    entering_exiting_vehicles = []  # List to store entering and exiting vehicles

    # Group by recordingId and trackId
    grouped_data = data.groupby(['recordingId', 'trackId'])

    print("------------ Analyzing vehicles ------------")

    # with pd.option_context('display.max_rows', 1,
    #                        'display.max_columns', 50,
    #                        'display.precision', 3,
    #                        'display.max_colwidth', 10000,
    #                        ):
    #     print(data)

    all_distance_info = []

    for (recordingId, trackId), group in tqdm(grouped_data, desc="Analyzing vehicles"):
    # for (recordingId, trackId), group in grouped_data:
        sorted_group = group.sort_values(by='frame')

        if check_hard_braking:
            # Perform hard braking check
            hard_braking_events = []
            # Extract frame numbers and velocities as separate arrays
            frame_numbers = sorted_group['frame'].values
            velocities = sorted_group['lonVelocity'].values

            # Combine them into a list of tuples
            velocity_data = list(zip(frame_numbers, velocities))
            hard_braking_detected, frame_range = is_hard_braking(velocity_data)

            if hard_braking_detected:
                hard_braking_events.append((trackId, frame_range))
                print(f"Hard braking detected for Track ID {trackId} in frames {frame_range}")



        lon_vel_increasing = calculate_mean_of_first_frames(sorted_group['lonVelocity'],
                                                            initial_frames_threshold) > speed_increase_threshold
        moving_to_lane_center = (sorted_group['latLaneCenterOffset'].abs() / sorted_group[
            'laneWidth']).mean() < lane_change_threshold
        lane_changing = sorted_group.head(initial_frames_threshold)['laneChange'].any()
        starting_from_lanelet_start = (sorted_group['traveledDistance'] <= sorted_group['laneletLength']).any()

        # same_lane_vehicles = filter_vehicles_in_same_lane(grouped_data, recordingId, trackId)


        # Check for vehicle interaction and relative velocity
        distance_info, close_vehicles_info, tailgating_info, yielding_info, entering_exiting_vehicles = check_vehicle_interaction_and_relative_velocity(grouped_data, recordingId,
                                                                                           trackId,
                                                                                           interaction_distance_threshold,
                                                                                           relative_speed_threshold, tailgating_distance_threshold, yielding_speed_threshold, yielding_distance_threshold, entering_exiting_vehicles)
        all_distance_info.append(distance_info)
        all_distance_info_filtered = list(filter(lambda x: x, all_distance_info))
        # print(close_vehicles_info)
        # if lon_vel_increasing or moving_to_lane_center or lane_changing or starting_from_lanelet_start or interaction_or_relative_velocity:
        #     data.loc[sorted_group.index, 'is_entering'] = True
        if lon_vel_increasing or moving_to_lane_center or lane_changing or starting_from_lanelet_start:
            data.loc[sorted_group.index, 'is_entering'] = True
    print("---record entering exiting---")
    print(entering_exiting_vehicles)
    print("---record entering exiting---")
    # print(all_distance_info_filtered)
    return data, all_distance_info_filtered


def check_vehicle_interaction_and_relative_velocity(grouped_data, current_recordingId, current_trackId, distance_threshold, speed_threshold, tailgating_distance_threshold, yielding_speed_threshold, yielding_distance_threshold, entering_exiting_vehicles):
    """
        Evaluates interactions between vehicles, focusing on relative speed, distance, and behaviors such as tailgating and yielding.

        grouped_data: Grouped DataFrame by recording and track ID for analysis.
        current_recordingId (int): ID of the current vehicle's recording session.
        current_trackId (int): Track ID of the current vehicle under analysis.
        distance_threshold (float): The maximum distance to consider for interaction detection.
        speed_threshold (float): The speed difference threshold to identify significant relative speed.
        tailgating_distance_threshold (float): Distance threshold below which a vehicle is considered to be tailgating.
        yielding_speed_threshold (float): Speed threshold to identify yielding behavior.
        yielding_distance_threshold (float): Distance threshold to identify yielding behavior.
        entering_exiting_vehicles (list): A list to record vehicles that are entering or exiting a lane.
        """
    current_group = grouped_data.get_group((current_recordingId, current_trackId))
    # Flatten the list of frame arrays to get all frame numbers
    all_frames = flatten_list_of_arrays(current_group['frame'].tolist())
    unique_frames = np.unique(all_frames)


    # with pd.option_context('display.max_rows', 4,
    #                        'display.max_columns', 24,
    #                        'display.precision', 3,
    #                        ):
    #     print(current_group)
    distance_info = {}
    tailgating_info = []
    yielding_info = []

    entering_exiting_contenders = []  # Initialize the list for special contenders

    for frame in unique_frames:

        frame_index = frame - unique_frames[0]  # Calculate the index
        # current_frame_data = current_group[np.isin(current_group['frame'].to_numpy(), np.array([frame]))]
        current_frame_data = current_group[filter_float_in_series_of_lists(current_group['frame'], frame)]

        current_velocity = current_frame_data['lonVelocity'].values[0][frame_index] if not current_frame_data.empty else None

        # # Check for hard braking
        # sorted_lon_velocities = current_frame_data['lonVelocity'].values
        #
        # if is_hard_braking(sorted_lon_velocities):
        #     hard_braking_info.append((current_trackId, frame))

        # Check if the lane changes
        behavior, frame = detect_lane_change_behavior(current_frame_data, frame_index, current_trackId)
        if behavior:
            print(f"Vehicle {current_trackId} likely {behavior} at frame {frame}")
            entering_exiting_vehicles.append((recordingId, current_trackId, "x", frame, "x", behavior))

        for (recordingId, trackId), group in grouped_data:
            # if recordingId == current_recordingId and trackId != current_trackId:
            if recordingId == current_recordingId and trackId > current_trackId:

                # other_frame_data = group[np.isin(group['frame'], frame)]
                other_frame_data = group[filter_float_in_series_of_lists(group['frame'], frame)]
                all_frames_2 = flatten_list_of_arrays(other_frame_data['frame'].tolist())
                unique_frames_2 = np.unique(all_frames_2)
                other_velocity = other_frame_data['lonVelocity'].values[0][frame-unique_frames_2[0]] if not other_frame_data.empty else None

                if not current_frame_data.empty and not other_frame_data.empty:
                    # Calculate the distance between the two vehicles

                    distance = np.sqrt((current_frame_data['xCenter'].values[0][frame_index] - other_frame_data['xCenter'].values[0][frame-unique_frames_2[0]])**2 +
                                       (current_frame_data['yCenter'].values[0][frame_index] - other_frame_data['yCenter'].values[0][frame-unique_frames_2[0]])**2)

                    # Check relative speed

                    if current_velocity is not None and other_velocity is not None:
                        relative_speed = current_velocity - other_velocity
                        # if relative_speed > speed_threshold:
                        #     print(
                        #         f"Vehicles {current_trackId} and {trackId} have significant relative speed (difference: {relative_speed}) at frame {frame}")

                    # Check yielding behavior
                    if is_yielding(distance, yielding_speed_threshold,
                                   yielding_distance_threshold, current_velocity, other_velocity):
                        yielding_info.append((current_trackId, trackId, frame))

                    # Check tailgating
                        leadDHW = current_frame_data['leadDHW'].values[0][
                            frame_index] if 'leadDHW' in current_frame_data.columns else None
                        if leadDHW is not None and is_tailgating(leadDHW, current_velocity, other_velocity,
                                                                 tailgating_distance_threshold, speed_threshold):
                            if (current_frame_data['odrRoadId'].values[0][frame_index] ==
                                    other_frame_data['odrRoadId'].values[0][frame - unique_frames_2[0]] and
                                    current_frame_data['odrLaneId'].values[0][frame_index] ==
                                    other_frame_data['odrLaneId'].values[0][frame - unique_frames_2[0]]):
                                if distance < distance_threshold:
                                    tailgating_info.append((current_trackId, trackId, frame))





                    # Check if vehicles are close enough to interact

                    if distance < distance_threshold:
                        pair_key = (current_trackId, trackId)
                        if pair_key not in distance_info:
                            if (current_frame_data['odrRoadId'].values[0][frame_index] ==
                                    other_frame_data['odrRoadId'].values[0][frame - unique_frames_2[0]] and current_frame_data['odrLaneId'].values[0][frame_index] ==
                                        other_frame_data['odrLaneId'].values[0][frame - unique_frames_2[0]]):
                                distance_info[pair_key] = []
                                # print(
                                #     f"Vehicles in the same lane: Track ID {current_trackId} and Track ID {trackId} at frame {frame}")
                                distance_tuple = (current_recordingId, current_trackId, trackId, frame, distance, current_frame_data['xVelocity'].values[0][frame_index], current_frame_data['yVelocity'].values[0][frame_index], other_frame_data['xVelocity'].values[0][frame_index], other_frame_data['yVelocity'].values[0][frame_index], current_frame_data['xAcceleration'].values[0][frame_index], current_frame_data['yAcceleration'].values[0][frame_index], other_frame_data['xAcceleration'].values[0][frame_index], other_frame_data['yAcceleration'].values[0][frame_index], current_frame_data['xCenter'].values[0][frame_index], current_frame_data['yCenter'].values[0][frame_index], other_frame_data['xCenter'].values[0][frame_index], other_frame_data['yCenter'].values[0][frame_index])
                                # Append the tuple to the distance_info for the pair key

                                if distance_tuple:
                                    if pair_key not in distance_info:
                                        distance_info[pair_key] = [distance_tuple]
                                    else:
                                        for i in range(frame_index - 5, frame_index + 6):
                                            if i >= 0 and i < len(all_frames):
                                                x_vel = current_frame_data['xVelocity'].values[0][
                                                    i] if 'xVelocity' in current_frame_data.columns else None
                                                y_vel = current_frame_data['yVelocity'].values[0][
                                                    i] if 'yVelocity' in current_frame_data.columns else None
                                                x_accel = current_frame_data['xAcceleration'].values[0][
                                                    i] if 'xAcceleration' in current_frame_data.columns else None
                                                y_accel = current_frame_data['yAcceleration'].values[0][
                                                    i] if 'yAcceleration' in current_frame_data.columns else None
                                                x_center = current_frame_data['xCenter'].values[0][
                                                    i] if 'xCenter' in current_frame_data.columns else None
                                                y_center = current_frame_data['yCenter'].values[0][
                                                    i] if 'yCenter' in current_frame_data.columns else None
                                                x_vel_other = other_frame_data['xVelocity'].values[0][
                                                    i] if 'xVelocity' in other_frame_data.columns else None
                                                y_vel_other = other_frame_data['yVelocity'].values[0][
                                                    i] if 'yVelocity' in other_frame_data.columns else None
                                                x_accel_other = other_frame_data['xAcceleration'].values[0][
                                                    i] if 'xAcceleration' in other_frame_data.columns else None
                                                y_accel_other = other_frame_data['yAcceleration'].values[0][
                                                    i] if 'yAcceleration' in other_frame_data.columns else None
                                                x_center_other = other_frame_data['xCenter'].values[0][
                                                    i] if 'xCenter' in other_frame_data.columns else None
                                                y_center_other = other_frame_data['yCenter'].values[0][
                                                    i] if 'yCenter' in other_frame_data.columns else None
                                                distance_tuple = (
                                                current_recordingId, current_trackId, trackId, i, distance, x_vel,
                                                y_vel,
                                                x_vel_other, y_vel_other,
                                                x_accel, y_accel,
                                                x_accel_other, y_accel_other,
                                                x_center, y_center,
                                                x_center_other, y_center_other
                                                )
                                                distance_info[pair_key].append(distance_tuple)
                                        # distance_info[pair_key].append(distance_tuple)
                                        # distance_info = [d for d in distance_info if d]
                                print(distance_info)

                        # print(f"Vehicles {current_trackId} and {trackId} are close (distance: {distance}) at frame {frame}")



    print(entering_exiting_contenders)




    close_vehicles_info = []

    for pair, dist_data in distance_info.items():
        decreasing, frame_range = is_distance_decreasing(dist_data)
        decreasing, dec_frame_range = is_distance_decreasing(dist_data)
        increasing, inc_frame_range = is_distance_increasing(dist_data)
        stable, stable_frame_range = is_distance_stable(dist_data)

        if decreasing:
            # print(f"Decreasing distance between vehicles {pair} from frame {dec_frame_range[0]} to {dec_frame_range[1]}")
            close_vehicles_info.append(pair)
        if increasing:
            # print(f"Increasing distance between vehicles {pair} from frame {inc_frame_range[0]} to {inc_frame_range[1]}")
            close_vehicles_info.append(pair)
        if stable:
            # print(f"Stable distance between vehicles {pair} from frame {stable_frame_range[0]} to {stable_frame_range[1]}")
            close_vehicles_info.append(pair)


    return distance_info, close_vehicles_info, tailgating_info, yielding_info, entering_exiting_vehicles


def is_distance_decreasing(distance_data, min_frames=3, decrease_threshold=0):
    """
        Check if the distance between two cars is consistently decreasing over frames.
        distance_data (list of tuples): List of tuples containing (frame, distance) data.
        min_frames (int): Minimum number of consecutive frames to consider for a valid trend.
        decrease_threshold (float): Minimum decrease in distance to consider it a significant decrease.
        Returns:
        bool, tuple: True and the range of frames if the distance is consistently decreasing, False and None otherwise.
        """
    if len(distance_data) < min_frames:
        return False, None

    sorted_data = sorted(distance_data, key=lambda x: x[3])  # Sorting by frame number
    distances = [d[4] for d in sorted_data]  # Extracting distance
    frames = [d[3] for d in sorted_data]  # Extracting frame number

    consecutive_decreases = 0
    start_frame = None

    for i in range(len(distances) - 1):
        if distances[i] - distances[i + 1] >= decrease_threshold:
            if consecutive_decreases == 0:
                start_frame = frames[i]
            consecutive_decreases += 1
            if consecutive_decreases >= min_frames - 1:
                return True, (start_frame, frames[i + 1])
        else:
            consecutive_decreases = 0

    return False, None

def is_distance_increasing(distance_data, min_frames=3, increase_threshold=0):
    """
        Check if the distance between two cars is consistently increasing over frames.
        distance_data (list of tuples): List of tuples containing (frame, distance) data.
        min_frames (int): Minimum number of consecutive frames to consider for a valid trend.
        increase_threshold (float): Minimum increase in distance to consider it a significant increase.
        Returns:
        bool, tuple: True and the range of frames if the distance is consistently increasing, False and None otherwise.
        """
    if len(distance_data) < min_frames:
        return False, None

    sorted_data = sorted(distance_data, key=lambda x: x[3])  # Sorting by frame number
    distances = [d[4] for d in sorted_data]  # Extracting distance
    frames = [d[3] for d in sorted_data]  # Extracting frame number

    consecutive_increases = 0
    start_frame = None

    for i in range(len(distances) - 1):
        if distances[i + 1] - distances[i] >= increase_threshold:
            if consecutive_increases == 0:
                start_frame = frames[i]
            consecutive_increases += 1
            if consecutive_increases >= min_frames - 1:
                return True, (start_frame, frames[i + 1])
        else:
            consecutive_increases = 0

    return False, None

def is_distance_stable(distance_data, min_frames=3, tolerance=1.0):
    """
        Check if the distance between two cars is stable (doesn't vary significantly) over frames.
        distance_data (list of tuples): List of tuples containing (frame, distance) data.
        min_frames (int): Minimum number of consecutive frames to consider for a valid stable trend.
        tolerance (float): The maximum allowed variation in distance to consider it stable.
        Returns:
        bool, tuple: True and the range of frames if the distance is stable, False and None otherwise.
    """
    if len(distance_data) < min_frames:
        return False, None

    sorted_data = sorted(distance_data, key=lambda x: x[3])  # Sorting by frame number
    distances = [d[4] for d in sorted_data]  # Extracting distance
    frames = [d[3] for d in sorted_data]  # Extracting frame number

    consecutive_stable = 0
    start_frame = None

    for i in range(len(distances) - 1):
        if abs(distances[i] - distances[i + 1]) <= tolerance:
            if consecutive_stable == 0:
                start_frame = frames[i]
            consecutive_stable += 1
            if consecutive_stable >= min_frames - 1:
                return True, (start_frame, frames[i + 1])
        else:
            consecutive_stable = 0

    return False, None

def is_tailgating(leadDHW, current_velocity, other_velocity, tailgating_distance_threshold, relative_speed_threshold):
    """
        Determine if a vehicle is tailgating another.
        leadDHW: Distance Headway.
        current_velocity, other_velocity: Longitudinal velocities of the current vehicle and the other vehicle.
        tailgating_distance_threshold: Threshold for considering a vehicle is too close.
        relative_speed_threshold: Threshold for considering a high relative speed.
    """
    return leadDHW < tailgating_distance_threshold and (current_velocity - other_velocity) > relative_speed_threshold

def filter_vehicles_in_same_lane(grouped_data, current_recordingId, current_trackId):
    """
        Filters and identifies vehicles within the same lane as the current vehicle over time.

        This function iterates through each frame for a specific vehicle identified by current_recordingId and trackId,
        comparing its lane positioning with other vehicles in the dataset to determine if they share the same lane at any point in time.

        grouped_data (DataFrameGroupBy): Grouped dataset by recordingId and trackId for efficient access.
        current_recordingId (int): The recording ID of the current focus vehicle.
        current_trackId (int): The track ID of the current focus vehicle.
        """
    current_group = grouped_data.get_group((current_recordingId, current_trackId))
    # Flatten the list of frame arrays to get all frame numbers
    all_frames = flatten_list_of_arrays(current_group['frame'].tolist())
    unique_frames = np.unique(all_frames)

    distance_info = {}
    for frame in unique_frames:

        frame_index = frame - unique_frames[0]  # Calculate the index
        # current_frame_data = current_group[np.isin(current_group['frame'].to_numpy(), np.array([frame]))]
        current_frame_data = current_group[filter_float_in_series_of_lists(current_group['frame'], frame)]

        current_velocity = current_frame_data['lonVelocity'].values[0][
            frame_index] if not current_frame_data.empty else None

        for (recordingId, trackId), group in grouped_data:
            # if recordingId == current_recordingId and trackId != current_trackId:
            if recordingId == current_recordingId and trackId > current_trackId:

                # other_frame_data = group[np.isin(group['frame'], frame)]
                other_frame_data = group[filter_float_in_series_of_lists(group['frame'], frame)]
                all_frames_2 = flatten_list_of_arrays(other_frame_data['frame'].tolist())
                unique_frames_2 = np.unique(all_frames_2)
                # print(unique_frames_2)
                # print(len(current_frame_data['lonVelocity'].values[0]) if not other_frame_data.empty else None)
                # print(len(other_frame_data['lonVelocity'].values[0]) if not other_frame_data.empty else None)
                # print(frame_index)

                if not current_frame_data.empty and not other_frame_data.empty:
                    if (current_frame_data['odrLaneId'].values[0][frame_index] == other_frame_data['odrLaneId'].values[0][frame-unique_frames_2[0]]):
                        pass


def is_yielding(distance, yielding_speed_threshold, yielding_distance_threshold, current_velocity, other_velocity):
    """
    Determine if a vehicle is yielding to another.
    - current_data, other_data: DataFrames for the current vehicle and the other vehicle.
    - yielding_speed_threshold: Threshold for significant speed reduction.
    - yielding_distance_threshold: Minimum distance for considering interaction.
    Returns:
    - True if the vehicle is yielding, False otherwise.
    """

    speed_diff = current_velocity - other_velocity
    return speed_diff < -yielding_speed_threshold and distance < yielding_distance_threshold

def is_hard_braking(velocity_data, min_frames=3, braking_acceleration_threshold=-2.0):
    """
    Check if a vehicle is performing hard braking over a series of frames.
    - velocity_data (list of tuples): List of tuples containing (frame, velocity) data.
    - min_frames (int): Minimum number of consecutive frames to consider for a valid braking trend.
    - braking_acceleration_threshold (float): Threshold for acceleration (negative for deceleration) to consider it hard braking (in m/s^2).
    Returns:
    - bool, tuple: True and the range of frames if hard braking is detected, False and None otherwise.
    """

    if len(velocity_data[0][1]) < min_frames:
        return False, None


    sorted_data = sorted(velocity_data, key=lambda x: x[0])

    velocities = [v for _, v in sorted_data]
    frames = [f for f, _ in sorted_data]

    consecutive_braking = 0
    start_frame = None

    for i in range(1, len(velocities[0])):

        acceleration = velocities[0][i] - velocities[0][i - 1]
        if acceleration <= braking_acceleration_threshold:
            if consecutive_braking == 0:
                start_frame = frames[0][i - 1]
            consecutive_braking += 1
            if consecutive_braking >= min_frames - 1:
                return True, (start_frame, frames[0][i])
        else:
            consecutive_braking = 0

    return False, None

def detect_lane_change_behavior(current_frame_data, frame_index, trackId):
    """
        Determines if a lane change event has occurred for a vehicle within the given frame.

        This function examines the lane ID, road ID, and section number at the current and previous frames
        to detect any changes, indicating a lane change event. The function categorizes the event as either
        'entering' or 'exiting' based on the direction of the lane change relative to the vehicle's current lane.

        current_frame_data (DataFrame): Data for the current vehicle at the specific frame.
        frame_index (int): The index of the current frame in the vehicle's trajectory.
        trackId (int): The identifier for the vehicle being analyzed.
        """
    # Initialize the result
    behavior = None

    # Check if the lane changes and the previous frame data exists
    if 'odrLaneId' in current_frame_data and frame_index > 0 and \
       (current_frame_data['odrLaneId'].values[0][frame_index] != current_frame_data['odrLaneId'].values[0][frame_index - 1] and
        current_frame_data['odrRoadId'].values[0][frame_index] != current_frame_data['odrRoadId'].values[0][frame_index - 1] and
        current_frame_data['odrSectionNo'].values[0][frame_index] != current_frame_data['odrSectionNo'].values[0][frame_index - 1]):

        print(f"Vehicle {trackId} changes lane at frame {frame_index}")

        # Determine if it's entering or exiting behavior
        if current_frame_data['odrLaneId'].values[0][frame_index] > current_frame_data['odrLaneId'].values[0][frame_index - 1]:
            behavior = "exiting"
        elif current_frame_data['odrLaneId'].values[0][frame_index] < current_frame_data['odrLaneId'].values[0][frame_index - 1]:
            behavior = "entering"

    return behavior, frame_index