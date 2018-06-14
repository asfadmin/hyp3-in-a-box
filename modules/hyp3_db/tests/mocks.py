# mocks.py
# Rohan Weeden
# Created: June 14, 2018

# Mock database


def mock_get_connection_str(user, password, host):
    return 'sqlite:///:memory:'
