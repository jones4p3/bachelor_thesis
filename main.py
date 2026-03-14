# --------- MAIN SCRIPT ---------

# Import necessary modules
import logging

import xarray as xr
from settings import setup_logging

xr.set_options(
    use_new_combine_kwarg_defaults=True
)  # Setting the data_vars = 'None' as default and not 'all'

print("\n--------- 1) Loading configuration files ---------")
from settings import load_radar_settings, load_dataset_settings, load_parameter_settings, print_parameter_settings

# Load radar settings and create RadarSettings objects for each radar
radar_settings_dict = load_radar_settings("settings/radar_settings.json")
print(f"✅ Radar settings loaded for: {list(radar_settings_dict.keys())}")

# Load dataset settings and create Dataset object
data = load_dataset_settings("settings/dataset_settings.json", radar_settings_dict)
print(f"✅ Dataset settings loaded with time range: {data.time_range}")
print(f"✅ Standard dimension names: {data.standard_dimension_names}")

# Load parameter settings
params = load_parameter_settings("settings/parameter_settings.json")
print_parameter_settings(params)

# Setting up the logging configuration
setup_logging(params)
logger = logging.getLogger("main")
logger.info("Logging setup completed with level: %s", params.logging_level)


# ------------------------------------------------------
# Loading the datasets and pre-processing them
# ------------------------------------------------------
logger.info("\n--------- 2) Loading the datasets and pre-processing ---------")
from pre_processing import load_and_preprocess_datasets

data = load_and_preprocess_datasets(data)
logger.info("✅ Datasets loaded and pre-processed for all radars.")


# ------------------------------------------------------
# Calculating occurrences and sensitivity before cleanup
# ------------------------------------------------------
logger.info(
    "\n--------- 3) Calculating occurrences and sensitivity before cleanup ---------"
)
from cleanup_and_alignment import calculate_occurrences_and_sensitivity_for_all_radars

data = calculate_occurrences_and_sensitivity_for_all_radars(data, params)
logger.info("✅ Occurrences and sensitivity calculated for all radars before cleanup.")


# ------------------------------------------------------
# Clean up and alignment of the datasets
# ------------------------------------------------------
from cleanup_and_alignment import cleanup_and_align_datasets
logger.info("\n--------- 4) Clean up and alignment of the datasets ---------")
radar_datasets = cleanup_and_align_datasets(data, params)
logger.info("✅ Datasets cleaned up and aligned.")


# ------------------------------------------
# CLOUD DETECTION ALGORITHM
# ------------------------------------------
logger.info("\n--------- 5) Running cloud detection algorithm ---------")
from cloud_detection import run_cloud_detection_algorithm
data = run_cloud_detection_algorithm(data, params)
logger.info("✅ Cloud detection algorithm completed for all radars.")


# ---------------------------------
# CLOUD STATISTICS
# ---------------------------------
logger.info("\n--------- 6) Calculating cloud statistics ---------")
from cloud_statistics import calculate_cloud_statistics
data = calculate_cloud_statistics(data, params)
logger.info("✅ Cloud statistics calculated for all radars.")

# ---------------------------------
# PLOTTING
# ---------------------------------
logger.info("\n--------- 7) Generating plots ---------")
from cloud_plotting import *
# Radar sensitivity profiles
plot_radar_sensitivity_profiles(radar_datasets)

# Time fraction profiles
plot_time_fraction_profiles(radar_datasets)

# Cloud fraction per height
plot_cloud_fraction(data)

# General vertical distribution of cloud layers
plot_general_vertical_distribution(data, plot_start_height=151)

# Per layer distribution of cloud base, cloud top, and cloud thickness
plot_per_layer_vertical_distribution(data, plot_start_height=151)

logger.info(f"✅ Plots generated and saved to {data.figure_folder}")