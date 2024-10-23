import os
import json
import random

try:
    from sonic_platform_base.psu_base import PsuBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class Psu(PsuBase):
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
        return self.name

    def get_psu_status(self):
        for item in self.metadata['chassis']['psus']:
            if item['name'] == self.name:
                return item['status_led']
        return None
    
    def get_presence(self):
        """
        Retrieves the presence status of power supply unit (PSU) defined

        Returns:
            bool: True if PSU is present, False if not
        """
        return True
    
    def get_voltage(self):
        """
        Retrieves current PSU voltage output

        Returns:
            A float number, the output voltage in volts,
            e.g. 12.1
        """
        return round(random.uniform(10.0, 12.0), 1)

    def get_current(self):
        """
        Retrieves present electric current supplied by PSU

        Returns:
            A float number, the electric current in amperes, e.g 15.4
        """
        return round(random.uniform(15.0, 20.0), 1)





