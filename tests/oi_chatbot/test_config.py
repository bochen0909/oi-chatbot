import os
import pytest
from oi_chatbot.config import load_config_file, OI_CHATBOT_HOME


def test_load_config_file():
    # Test case 1: Test loading config file with valid filepath
    profiles, default_profile = load_config_file('config.yml')
    assert isinstance(profiles, dict)
    assert isinstance(default_profile, dict)

    # Test case 2: Test loading config file with invalid filepath
    with pytest.raises(FileNotFoundError):
        load_config_file('invalid_config.yml')


def test_oi_chatbot_home():
    # Test case 3: Test if OI_CHATBOT_HOME directory is created
    assert os.path.exists(OI_CHATBOT_HOME)


if __name__ == '__main__':
    pytest.main()
