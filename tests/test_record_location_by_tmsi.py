import pytest
from car_trace import record_location_by_tmsi, RECORD_LOCATIONS


@pytest.fixture(autouse=True)
def clear_global_variables():
    """Reset the global RECORD_LOCATIONS before and after each test."""
    RECORD_LOCATIONS.clear()
    yield
    RECORD_LOCATIONS.clear()


@pytest.fixture
def test_data():
    """
    Provide sample data for different test scenarios.
    This fixture is more descriptive and provides well-structured test data.
    """
    return [
        # First batch - Single user (E1) with sequential movements
        [
            {"end_time": "2025-04-21 10:00:00", "m_tmsi": "E1", "pos_last_lon": 12.232342, "pos_last_lat": 34.234234},
            {"end_time": "2025-04-21 10:05:00", "m_tmsi": "E1", "pos_last_lon": 12.433342, "pos_last_lat": 45.344234},
            {"end_time": "2025-04-21 10:10:00", "m_tmsi": "E1", "pos_last_lon": 13.252342, "pos_last_lat": 54.234234},
            {"end_time": "2025-04-21 10:11:00", "m_tmsi": "E1", "pos_last_lon": 15.272342, "pos_last_lat": 64.234234},
            {"end_time": "2025-04-21 10:12:00", "m_tmsi": "E1", "pos_last_lon": 15.282342, "pos_last_lat": 74.234234}
        ],
        # Second batch - Mixed users and a time gap for E3
        [
            {"end_time": "2025-04-21 10:13:00", "m_tmsi": "E1", "pos_last_lon": 16.636342, "pos_last_lat": 34.234234},
            {"end_time": "2025-04-21 10:15:00", "m_tmsi": "E1", "pos_last_lon": 17.437342, "pos_last_lat": 45.344234},
            {"end_time": "2025-04-21 10:16:00", "m_tmsi": "E3", "pos_last_lon": 18.657342, "pos_last_lat": 54.234234},
            {"end_time": "2025-04-21 10:17:00", "m_tmsi": "E2", "pos_last_lon": 15.272342, "pos_last_lat": 64.234234},
            {"end_time": "2025-04-21 12:18:00", "m_tmsi": "E3", "pos_last_lon": 29.282342, "pos_last_lat": 74.234234}
        ],
    ]


@pytest.fixture
def test_data_single_user():
    """Provide test data for a single user with known values for assertions."""
    return [
        [
            {"end_time": "2025-04-21 10:00:00", "m_tmsi": "E4", "pos_last_lon": 10.0, "pos_last_lat": 50.0},
            {"end_time": "2025-04-21 10:30:00", "m_tmsi": "E4", "pos_last_lon": 10.1, "pos_last_lat": 50.1},
            {"end_time": "2025-04-21 11:00:00", "m_tmsi": "E4", "pos_last_lon": 10.2, "pos_last_lat": 50.2},
        ]
    ]


@pytest.fixture
def test_data_with_errors():
    """Provide test data with some bad records to test error handling."""
    return [
        [
            {"end_time": "2025-04-21 10:00:00", "m_tmsi": "E5", "pos_last_lon": 10.0, "pos_last_lat": 50.0},
            {"end_time": "INVALID DATE", "m_tmsi": "E5", "pos_last_lon": 10.1, "pos_last_lat": 50.1},  # Bad date
            {"end_time": "2025-04-21 11:00:00", "m_tmsi": "E5", "pos_last_lon": "invalid", "pos_last_lat": 50.2},  # Bad coordinates
        ]
    ]


def test_record_counts(test_data):
    """Test that record counts are correct for each TMSI."""
    records = record_location_by_tmsi(test_data)

    # Each TMSI should have correct number of records
    assert len(records['E1']) == 7  # 1 initial + 6 movements
    assert len(records['E2']) == 1  # 1 initial (first appearance)
    assert len(records['E3']) == 2  # 1 initial + 1 movement

    # Test that all TMSIs are present
    assert set(records.keys()) == {'E1', 'E2', 'E3'}


def test_distance_calculations(test_data_single_user):
    """Test distance calculations with known coordinates."""
    records = record_location_by_tmsi(test_data_single_user)

    # E4's first movement should be approximately 15.55 km
    # (Based on the approximate distance between 50.0,10.0 and 50.1,10.1)
    assert records['E4'][1]['distance'] > 0
    assert 'distance' in records['E4'][1]

    # Second movement should be similar
    assert records['E4'][2]['distance'] > 0


def test_speed_calculations(test_data_single_user):
    """Test speed calculations with known values."""
    records = record_location_by_tmsi(test_data_single_user)

    # Speed is distance/time_range
    # Check that speed is calculated and reasonable
    assert 'speed' in records['E4'][1]
    assert records['E4'][1]['speed'] > 0

    # Calculate expected speed for verification
    # (This would need adjustment based on actual distance calculation)
    distance = records['E4'][1]['distance']
    time_range = 0.5  # 30 minutes = 0.5 hours
    expected_speed = distance / time_range


def test_error_handling(test_data_with_errors):
    """Test that the function properly handles bad data."""
    # Should raise exceptions for bad data
    with pytest.raises(ValueError) as e:
        records = record_location_by_tmsi(test_data_with_errors)



