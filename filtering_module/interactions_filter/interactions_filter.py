# from utilities.data_loading import load_exid_data, load_round_data, load_inD_data
from .exiting_behaviour import detect_exiting_vehicles
from .overtaking import detect_overtaking
from .entering_behaviour import detect_entering_vehicles
from .yielding_behaviour import filter_yielding_behaviour
from .speed_adjustment import filter_speed_adjustment
from .lane_changing import detect_lane_changes


class InteractionsFilter:
    """
        A class designed to filter and analyze vehicle interactions from traffic data sets.
        This includes detecting exiting and entering behaviors, overtaking, merging onto exit ramps,
        yielding behavior, speed adjustments, and lane changes.
        """
    def __init__(self):
        pass

    def detect_exiting_vehicles(self, exid_data):
        """
                Detects vehicles exiting a roadway or lane.
                """
        return detect_exiting_vehicles(exid_data)

    def detect_entering_vehicles(self, exid_data, interaction_distance_threshold, relative_speed_threshold, tailgating_distance_threshold, yielding_speed_threshold, yielding_distance_threshold):
        """
                Detects vehicles entering a roadway or lane based on specified thresholds.
                """
        return detect_entering_vehicles(exid_data)

    def detect_overtaking(self, exid_data, interaction_distance_threshold, relative_speed_threshold, position_change_threshold):
        """
                Detects overtaking maneuvers based on specified thresholds.
                """
        return detect_overtaking(exid_data)

    def filter_yielding_behavior(self, exid_data):
        """
                Identifies vehicles exhibiting yielding behavior.
                """
        return filter_yielding_behaviour(exid_data)

    def filter_speed_adjustment(self, exid_data):
        """
                Detects speed adjustment behavior among vehicles.
                """
        return filter_speed_adjustment(exid_data)

    def lane_changing(self, exid_data):
        """
                Detects lane changing actions among vehicles.
                """
        return detect_lane_changes(exid_data)