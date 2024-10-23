# Description: Module contains the definitions of SONiC platform APIs
# which provide the chassis specific details
#
# Copyright (c) 2019, Nokia
# All rights reserved.
#
import os
import json

try:
    from sonic_platform_base.chassis_base import ChassisBase
    from .module import Module
    from .psu import Psu
    from .fan_drawer import FanDrawer
    from .thermal import Thermal

except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class Chassis(ChassisBase):
    """
    VS Platform-specific Chassis class
    """
    def __init__(self):
        ChassisBase.__init__(self)
        self.metadata_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'ot_vs_chassis_metadata.json' )
        self.metadata = self._read_metadata()
        for item in self.metadata['chassis']['modules']:
            self._module_list.append(Module(self, item['name']))
        for item in self.metadata['chassis']['psus']:
            self._psu_list.append(Psu(self, item['name']))
        for item in self.metadata['chassis']['fan_drawers']:
            self._fan_drawer_list.append(FanDrawer(self, item['name']))
        for item in self.metadata['chassis']['thermals']:
            self._thermal_list.append(Thermal(self, item['name']))

    def _read_metadata(self):
        metadata = {}
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
        else:
            raise FileNotFoundError("Metadata file {} not found".format(self.metadata_file))
        return metadata

    def get_my_slot(self):
        return len(self.metadata['chassis']['modules']) - 1

    def get_supervisor_slot(self):
        return 1

    def get_name(self):
        return self.metadata['chassis']['name']

    def get_description(self):
        return self.metadata['chassis']['description']

