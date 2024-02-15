import pandas as pd

def detect_lane_changes(data):
    """
    Detect lane changes for each vehicle in the dataset based on changes in the odrLaneId,
    and print the trackId and frame number when a lane change is detected.
    :param data: DataFrame containing the dataset.
    :return: A DataFrame with lane change events marked and printed.
    """
    # Add a column to mark lane changes
    data['is_lane_changing'] = False

    # Group by recordingId and trackId
    grouped_data = data.groupby(['recordingId', 'trackId'])

    # Iterate through each group
    for (recordingId, trackId), group in grouped_data:
        # Shift the odrLaneId to compare with the next frame
        shifted_lane_id = group['odrLaneId'].shift(-1)

        # Detect lane change when the lane id changes between consecutive frames
        lane_change_detected = (group['odrLaneId'] != shifted_lane_id) & (group['odrLaneId'].notna()) & (shifted_lane_id.notna())

        # Update the is_lane_changing column and print if lane change is detected
        for idx, change in lane_change_detected.iteritems():
            if change:
                print(f"Lane change detected for Track ID {trackId} at Frame {group.loc[idx, 'frame']}")
                data.at[idx, 'is_lane_changing'] = True

    return data