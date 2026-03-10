from dataclasses import dataclass

@dataclass
class RadarAttributes:
    """Class to hold radar attributes information"""
    name: str
    frequency: str
    band: str

@dataclass
class RadarDimensions:
    """Class to hold radar dimension names information"""
    time: str
    height: str
    ze: str

@dataclass
class RadarSettings:
    """Class to hold radar settings information"""
    slug: str
    data_path: str
    attributes: RadarAttributes
    convert_linear_to_dBZ: bool
    add_to_range: bool
    vars_to_keep: list
    dimension_names: RadarDimensions