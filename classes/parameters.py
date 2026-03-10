from dataclasses import dataclass

@dataclass
class SensitivityParameters:
    """Class to hold parameters for sensitivity calculation"""
    threshold: float
    min_samples_per_height: float

@dataclass
class OccurrenceParameters:
    """Class to hold parameters for occurrence calculation"""
    bin_size: float

@dataclass
class Parameters:
    """Class to hold parameters for the analysis"""
    sensitivity: SensitivityParameters
    occurrence: OccurrenceParameters