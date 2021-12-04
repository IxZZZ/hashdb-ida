import pytest
from hashdb.types.enum_value import EnumValue


@pytest.fixture
def valid_algorithms_data():
    yield {'algorithms': [
        {'algorithm': 'crc32', 'description': 'Standard crc32 hash.', 'type': 'unsigned_int'},
        {'algorithm': 'fnv1a_64', 'description': 'FNV1a hash (64-bit)', 'type': 'unsigned_long'}]}


@pytest.fixture
def invalid_algorithms_data():
    yield {'algorithms': [
        {},  # empty object
        #  missing description
        {'algorithm': 'crc32'},
        #  missing type
        {'algorithm': 'crc32', 'description': 'Standard crc32 hash.'},
        #  invalid type
        {'algorithm': 'crc32', 'description': 'Standard crc32 hash.', 'type': 'unsigned_float'}]}


@pytest.fixture
def valid_hash_data():
    yield {'hashes': [{'hash': 1653273962, 'string': {'string': 'RouteTheCall', 'is_api': True,
                                                      'permutation': 'api', 'api': 'RouteTheCall',
                                                      'modules': ['zipfldr']}},
                      {'hash': 2998556761, 'string': {'string': 'DllCanUnloadNow', 'is_api': False}}]}


@pytest.fixture
def invalid_hash_data():
    yield {'hashes': [{},  # empty object
                      # missing string object
                      {'hash': 1653273962},
                      # missing "is_api" in the string object
                      {'hash': 1075368562, 'string':
                          {'string': 'DllGetClassObject'}},
                      # missing permutation value
                      {'hash': 1075368562, 'string':
                          {'string': 'DllGetClassObject',
                           'is_api': True}},
                      # api value != string value
                      {'hash': 1075368562, 'string':
                          {'string': 'DllGetClassObject',
                           'is_api': True,
                           'permutation': 'api',
                           'api': 'DllGetClassObject_12345'}},
                      # missing "modules"
                      {'hash': 1075368562, 'string':
                          {'string': 'DllGetClassObject',
                           'is_api': True,
                           'permutation': 'api',
                           'api': 'DllGetClassObject'}}]}


@pytest.fixture
def valid_hits_data():
    yield {'hits': [{'algorithm': 'crc32', 'count': 1, 'hitrate': 1.0}]}


@pytest.fixture
def invalid_hits_data():
    yield {'hits': [
        {},  # empty object
        # missing count
        {'algorithm': 'crc32'},
        # missing hitrate
        {'algorithm': 'crc32', 'count': 1}
    ]}


@pytest.fixture
def enum_values():
    yield (
        EnumValue(name="invalid name", value=12345, is_api=False),
        EnumValue(name="taken_name", value=12345, is_api=False),
        EnumValue(name="missing_suffix", value=12345, is_api=True))


@pytest.fixture
def expected_enum_values():
    yield (
        EnumValue(name="invalid_name", value=12345, is_api=False),
        EnumValue(name="taken_name_5", value=12345, is_api=False),
        EnumValue(name="missing_suffix_2", value=12345, is_api=True))
