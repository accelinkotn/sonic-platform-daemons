import os
import json

try:
    from sonic_platform_base.component_base import ComponentBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class Component(ComponentBase):
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

    def get_name(self):
        return str(self.name)

    def get_description(self):
        for item in self.metadata['chassis']['modules']['components']:
            if item['name'] == self.name:
                return item['description']
        return ""
