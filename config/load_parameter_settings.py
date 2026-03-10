import json
import sys
from classes import Parameters, SensitivityParameters, OccurrenceParameters



def load_parameter_settings(parameter_settings_path):
    try:
        with open(parameter_settings_path, 'r') as f:
            parameter_settings = json.load(f)
        
        sensitivty_params = SensitivityParameters(**parameter_settings.get("sensitivity", False))
        occurrence_params = OccurrenceParameters(**parameter_settings.get("occurrence", False))

        params = Parameters(
            sensitivity=sensitivty_params,
            occurrence=occurrence_params
        )
        return params
    except Exception as e:
        print(f"Error loading parameter settings: {e}")
        sys.exit(1)
        return None
    