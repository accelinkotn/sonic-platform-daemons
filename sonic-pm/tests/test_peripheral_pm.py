import os
import sys
from imp import load_source  
import pytest
from unittest.mock import MagicMock, patch,call
from unittest import mock
from datetime import datetime, timedelta
import threading
import time
from swsscommon import swsscommon


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

# 导入 peripheral_pm 中的模块和类
from peripheral_pm import PerformanceStats, get_nearest_15min, PM_UPDATE_PERIOD_SECS, device_attributes


@pytest.fixture
def performance_stats():
    return PerformanceStats("test_identifier")


@pytest.fixture
def mock_device():
    class MockDevice:
        def get_voltage(self):
            return 12.3

        def get_current(self):
            return 2.4

        def get_speed(self):
            return 5000

        def get_presence(self):
            return True

    return MockDevice()

@pytest.fixture
def devicedata():
    return {
        'name': 'PSU_0',
        'attr_list': ['voltage', 'current'],
        'stats': {
            'voltage': {
                'startime_15min': datetime(2023, 10, 1, 12, 0),
                'current_15min_value': 12.3,
                'avg_15min_value': 12.3,
                'max_15min_value': 12.3,
                'max_15min_timestamp': datetime(2023, 10, 1, 12, 0),
                'min_15min_value': 12.3,
                'min_15min_timestamp': datetime(2023, 10, 1, 12, 0),
                'startime_24hr': datetime(2023, 10, 1, 0, 0),
                'current_24hr_value': 12.3,
                'avg_24hr_value': 12.3,
                'max_24hr_value': 12.3,
                'max_24hr_timestamp': datetime(2023, 10, 1, 12, 0),
                'min_24hr_value': 12.3,
                'min_24hr_timestamp': datetime(2023, 10, 1, 12, 0)
            },
            'current': {
                'startime_15min': datetime(2023, 10, 1, 12, 0),
                'current_15min_value': 2.4,
                'avg_15min_value': 2.4,
                'max_15min_value': 2.4,
                'max_15min_timestamp': datetime(2023, 10, 1, 12, 0),
                'min_15min_value': 2.4,
                'min_15min_timestamp': datetime(2023, 10, 1, 12, 0),
                'startime_24hr': datetime(2023, 10, 1, 0, 0),
                'current_24hr_value': 2.4,
                'avg_24hr_value': 2.4,
                'max_24hr_value': 2.4,
                'max_24hr_timestamp': datetime(2023, 10, 1, 12, 0),
                'min_24hr_value': 2.4,
                'min_24hr_timestamp': datetime(2023, 10, 1, 12, 0)
            }
        }
    }


def test_get_nearest_15min():
    now = datetime(2023, 10, 1, 12, 7)
    assert get_nearest_15min(now) == datetime(2023, 10, 1, 12, 0)

    now = datetime(2023, 10, 1, 12, 22)
    assert get_nearest_15min(now) == datetime(2023, 10, 1, 12, 15)

    now = datetime(2023, 10, 1, 12, 38)
    assert get_nearest_15min(now) == datetime(2023, 10, 1, 12, 30)

    now = datetime(2023, 10, 1, 12, 53)
    assert get_nearest_15min(now) == datetime(2023, 10, 1, 12, 45)


def test_add_device(performance_stats, mock_device):
    performance_stats.add_device("PSU_0", mock_device)
    assert "PSU_0" in performance_stats.stats
    assert performance_stats.stats["PSU_0"]["obj"] == mock_device
    assert "voltage" in performance_stats.stats["PSU_0"]["attr_list"]
    assert "current" in performance_stats.stats["PSU_0"]["attr_list"]


def test_initialize_properties(performance_stats):
    props = performance_stats.initialize_properties()
    assert props["startime_15min"] is None
    assert props["current_15min_value"] is None
    assert props["max_15min_value"] is None
    assert props["max_15min_timestamp"] is None
    assert props["min_15min_value"] is None
    assert props["min_15min_timestamp"] is None
    assert props["value_sum_15min_value"] == 0
    assert props["value_count_15min"] == 0
    assert props["avg_15min_value"] == 0
    assert props["last_15min_reset"] is None

    assert props["startime_24hr"] is None
    assert props["current_24hr_value"] is None
    assert props["max_24hr_value"] is None
    assert props["max_24hr_timestamp"] is None
    assert props["min_24hr_value"] is None
    assert props["min_24hr_timestamp"] is None
    assert props["value_sum_24hr_value"] == 0
    assert props["value_count_24hr"] == 0
    assert props["avg_24hr_value"] == 0
    assert props["last_24hr_reset"] is None


@patch('peripheral_pm.datetime')
def test_update_stats(mock_datetime, performance_stats, mock_device):
    mock_datetime.now.return_value = datetime(2023, 10, 1, 12, 0)
    performance_stats.add_device("PSU_0", mock_device)
    stats = performance_stats.stats["PSU_0"]["stats"]["voltage"]

    # 初始化 startime_15min
    stats["startime_15min"] = datetime(2023, 10, 1, 12, 0)

    performance_stats.update_stats(stats, 12.3, datetime(2023, 10, 1, 12, 0), 1)
    assert stats["current_15min_value"] == 12.3
    assert stats["max_15min_value"] == 12.3
    assert stats["min_15min_value"] == 12.3
    assert stats["last_15min_reset"] == datetime(2023, 10, 1, 12, 0)
    assert stats["startime_15min"] == datetime(2023, 10, 1, 12, 0)

    performance_stats.update_stats(stats, 12.5, datetime(2023, 10, 1, 12, 1), 1)
    assert stats["current_15min_value"] == 12.5
    assert stats["max_15min_value"] == 12.5
    assert stats["min_15min_value"] == 12.3
    assert stats["last_15min_reset"] == datetime(2023, 10, 1, 12, 0)
    assert stats["startime_15min"] == datetime(2023, 10, 1, 12, 0)





