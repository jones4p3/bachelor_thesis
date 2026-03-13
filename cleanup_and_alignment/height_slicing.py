import numpy as np
import logging

logger = logging.getLogger("height_slicing")

def slice_height_range(data):
    highest_minimum_height = {"radar": "", "height": -np.inf}
    lowest_maximum_height = {"radar": "", "height": np.inf}
    for radar, ds in data.radar_datasets.items():
        logger.debug(f"  ---------------- Processing radar: {radar} ----------------")
        height = ds["height"].values
        min_height = height.min()
        max_height = height.max()
        logger.debug(f"    Min height: {min_height} m")
        logger.debug(f"    Max height: {max_height} m")
        if min_height > highest_minimum_height["height"]:
            highest_minimum_height["radar"] = radar
            highest_minimum_height["height"] = min_height
        if max_height < lowest_maximum_height["height"]:
            lowest_maximum_height["radar"] = radar
            lowest_maximum_height["height"] = max_height
        logger.debug(
            f"Radar with lowest min height: {highest_minimum_height['radar']} at {highest_minimum_height['height']} m"
        )
        logger.debug(
            f"Radar with highest max height: {lowest_maximum_height['radar']} at {lowest_maximum_height['height']} m"
        )

    # Slcing the dataset to common height range
    common_min_height = highest_minimum_height["height"]
    common_max_height = lowest_maximum_height["height"]
    logger.debug(
        f"Common height range for all radars: {common_min_height:.2f} m to {common_max_height:.2f} m"
    )

    for radar, ds in data.radar_datasets.items():
        logger.debug(f"  ---------------- Slicing radar: {radar} ----------------")
        height_size = ds["height"].size
        height_1d = np.asarray(ds["height"].values).squeeze()
        idx = np.where(
            (height_1d >= common_min_height) & (height_1d <= common_max_height)
        )[0]
        i0, i1 = idx[0], idx[-1] + 1  # +1 to include the last index

        # Mask the heights within the common range
        ds_sliced = ds.isel(height=slice(i0, i1))
        new_min_height = ds_sliced["height"].min().values
        new_max_height = ds_sliced["height"].max().values
        logger.debug(f"Original height size: {height_size} gates")
        logger.debug(f"Sliced height size: {ds_sliced['height'].size} gates")
        logger.debug(f"    New min height: {new_min_height} m")
        logger.debug(f"    New max height: {new_max_height} m")
        data.radar_datasets[radar] = ds_sliced
        
    return data, highest_minimum_height, lowest_maximum_height