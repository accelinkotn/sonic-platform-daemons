import os
import json

try:
    from sonic_platform_base.thermal_base import ThermalBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class Thermal(ThermalBase):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.metadata_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'ot_vs_chassis_metadata.json' )
        self.metadata = self._read_metadata()

    def _read_metadata(self):
        metadata = {}
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
        else:
            raise FileNotFoundError("Metadata file {} not found".format(self.metadata_file))
        return metadata

    def get_high_critical_threshold(self):
        for item in self.metadata['chassis']['thermals']:
            if item['name'] == self.name:
                return item['high-crit-threshold']
        return 0

    def get_low_critical_threshold(self):
        for item in self.metadata['chassis']['thermals']:
            if item['name'] == self.name:
                return item['low-crit-threshold']
        return 0

    def get_minimum_recorded(self):
        for item in self.metadata['chassis']['thermals']:
            if item['name'] == self.name:
                return item['maximum-recorded']
        return 0

    def get_maximum_recorded(self):
        for item in self.metadata['chassis']['thermals']:
            if item['name'] == self.name:
                return item['minimum-recorded']
        return 0
