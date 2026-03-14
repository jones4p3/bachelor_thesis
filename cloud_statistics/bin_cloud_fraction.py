import numpy as np
import xarray as xr
import logging
logger = logging.getLogger("cloud_statistics")

def bin_cloud_fraction(data, params):
    bin_size = 100  # Bin size in meters
    max_height = 10800  # Maximum height to consider in meters
    bin_edges = np.arange(bin_size, max_height + bin_size, bin_size)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    n_bins = len(bin_centers)
    logger.info(f"🗑️  Binning cloud fraction into {n_bins} bins of size {bin_size} m up to {max_height} m.")

    for (radar_slug, ds) in data.radar_datasets.items():
        logger.debug(f"Calculating binned cloud fraction for radar: {radar_slug}")
        height = ds["height"].values
        gate_thickness = ds["range_gate_sizes"].values.astype("float32") # Ensure gate thickness is float for weighting
        cloud_in_gate = ds["cloud_in_gate"].values
        time = ds["time"].values
        n_time = len(time)
        logger.debug(f"Number of time steps: {n_time}")
    
        # Output array
        cloud_fraction_binned = np.full((n_time, n_bins), np.nan, dtype=float)

        for time_step in range(n_time): #n_time
            if time_step % 100 == 0:
                logger.debug(f"Processing time index {time_step+1}/{n_time}", end="\r")
            cloudy = cloud_in_gate[time_step].astype(float)

            # Skip empty profiles
            if np.all(np.isnan(cloudy)):
                logger.debug(f" No clouds detected, skipping time step [{time_step}].")
                continue

            # Calculate thickness per bin
            cloudy_thickness, counts_thickness = np.histogram(height, bins=bin_edges, weights=gate_thickness * cloudy) # Weight: "Count only the cloudy part of each gate in meters"

            # Calculate total thickness per bin
            total_thickness, counts_total = np.histogram(height, bins=bin_edges, weights=gate_thickness) # Weight: "Count the entire observed thickness, cloudy or not"
            # Calculate cloud fraction per bin
            valid_bins = total_thickness > 0
            cloud_fraction_binned[time_step, valid_bins] = (cloudy_thickness[valid_bins] / total_thickness[valid_bins]) # What fraction of the bin's total thickness is cloudy

        cloud_fraction_binned_da = xr.DataArray(
            cloud_fraction_binned,
            dims=["time", "height_bin"],
            coords={
                "time": ds["time"],
                "height_bin": bin_centers
            },
            name="cloud_fraction_binned",
            attrs={
                "description": f"Cloud fraction per height bin weighted by gate thickness and binned in {bin_size} m height bins",
                "units": "fraction (0-1)"
            }
        )   

        ds["cloud_fraction_binned"] = cloud_fraction_binned_da
        data.radar_datasets[radar_slug] = ds

    logger.info("🗑️  ✅ Cloud fraction binned for all radars.")
    return data
