import os
import json

try:
    from sonic_platform_base.fan_drawer_base import FanDrawerBase
    from .fan import Fan
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class FanDrawer(FanDrawerBase):
    def __init__(self, parent, name):
        self._fan_list = []
        self.parent = parent
        self.name = name
        self.metadata_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'ot_vs_chassis_metadata.json' )
        self.metadata = self._read_metadata()
        for item in self.metadata['chassis']['fan_drawers']:
            if item['name'] == self.name:
                for item2 in item['fans']:
                    self._fan_list.append(Fan(self, item2['name']))

    def _read_metadata(self):
        metadata = {}
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
        else:
            raise FileNotFoundError("Metadata file {} not found".format(self.metadata_file))
        return metadata
