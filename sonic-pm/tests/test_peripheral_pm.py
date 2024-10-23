import os
import sys
from imp import load_source  
import pytest
from unittest.mock import MagicMock, patch
from unittest import mock
from datetime import datetime, timedelta
import threading
import time


tests_path = os.path.dirname(os.path.abspath(__file__))

# Add mocked_libs path so that the file under test can load mocked modules from there
mocked_libs_path = os.path.join(tests_path, "mocked_libs")
sys.path.insert(0, mocked_libs_path)

from sonic_py_common import daemon_base
daemon_base.db_connect = mock.MagicMock()

# Add path to the file under test so that we can load it
modules_path = os.path.dirname(tests_path)
scripts_path = os.path.join(modules_path, "scripts")
sys.path.insert(0, modules_path)
load_source('peripheral_pm', os.path.join(scripts_path, 'peripheral_pm'))

from peripheral_pm import PerformanceStats, get_nearest_15min, PM_UPDATE_PERIOD_SECS


def test_get_nearest_15min():
    now = datetime(2023, 10, 1, 12, 34, 56)
    assert get_nearest_15min(now) == datetime(2023, 10, 1, 12, 30)

    now = datetime(2023, 10, 1, 12, 7, 56)
    assert get_nearest_15min(now) == datetime(2023, 10, 1, 12, 0)

    now = datetime(2023, 10, 1, 12, 22, 56)
    assert get_nearest_15min(now) == datetime(2023, 10, 1, 12, 15)

    now = datetime(2023, 10, 1, 12, 46, 56)
    assert get_nearest_15min(now) == datetime(2023, 10, 1, 12, 45)







