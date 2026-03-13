# ------------------------------------------------------
# Clean up and alignment of the datasets
# ------------------------------------------------------
from .time_matching import time_match_radars, remove_downtime_intervals_from_ds
from .height_slicing import slice_height_range
from .range_gate_resolution import calculate_range_gate_resolution
import logging

logger = logging.getLogger("cleanup_and_alignment")

# Set the arrays for storing results
combined_downtime = []
combined_uptime = []
combined_assumed_starting_seconds = 0
combined_longer_than_30_seconds_counts = 0


def cleanup_and_align_datasets(data, params):
    # ---------------------
    # Time matching radars
    # ---------------------
    logger.info("⏱️  Time-matching radars based on uptime...")
    uptime_results = time_match_radars(data, params)
    logger.info("⏱️  ✅ Time-matching completed. Uptime results calculated for all radars.")

    # ---------------------
    # Height slicing
    # ---------------------
    logger.info("🗼 Height slicing...")
    data, highest_minimum_height, lowest_maximum_height = slice_height_range(data)
    logger.info("🗼 ✅ Height slicing completed.")

    # -------------------------------------------------------
    # RANGE GATE RESOLUTION
    # -------------------------------------------------------
    logger.info("📏 Calculating range gate resolution and adding it to the datasets...")
    data, unique_range_gate_sizes = calculate_range_gate_resolution(data)
    logger.info("📏 ✅ Range gate resolution calculated.")

    # -------------------------------------------------------
    # Cleaning
    # -------------------------------------------------------
    logger.info("🧹 Removing downtime intervals from the datasets...")
    data = remove_downtime_intervals_from_ds(data, params, highest_minimum_height, lowest_maximum_height, unique_range_gate_sizes, uptime_results)
    logger.info("🧹 ✅ Downtime intervals removed from the datasets.")

    return data
    