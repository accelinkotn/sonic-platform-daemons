import os
import json

try:
    from sonic_platform_base.module_base import ModuleBase
    from .component import Component
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class Module(ModuleBase):
    def __init__(self, parent, name):
        # ModuleBase.__init__(self)
        self._component_list = []
        self.metadata_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'ot_vs_chassis_metadata.json' )
        self.metadata = self._read_metadata()
        self.name = name
        for item in self.metadata['chassis']['modules']:
            if item['name'] == name:
                for item2 in item['components']:
                    self._component_list.append(Component(self, item2['name']))

    def _read_metadata(self):
        metadata = {}
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
        else:
            raise FileNotFoundError("Metadata file {} not found".format(self.metadata_file))
        return metadata

    def get_name(self):
        return self.name

    def get_description(self):
        for item in self.metadata['chassis']['modules']:
            if item['name'] == self.name:
                return item['description']
        return None

    def get_oper_status(self):
        for item in self.metadata['chassis']['modules']:
            if item['name'] == self.name:
                return item['module-status']
        return None

    def get_type(self):
        for item in self.metadata['chassis']['modules']:
            if item['name'] == self.name:
                if item['name'] == "SUPERVISOR0":
                    return self.MODULE_TYPE_SUPERVISOR
                else:
                    return self.MODULE_TYPE_LINE
