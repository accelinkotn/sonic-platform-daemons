import os
import json
import random

try:
    from sonic_platform_base.fan_base import FanBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class Fan(FanBase):
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

    def get_speed(self): 
        return round(random.randint(1000, 5000))

    def get_status_led(self):
        for item in self.metadata['chassis']['fan_drawers']['fans']:
            if item['name'] == self.name:
                return item['status_led']
        return None
