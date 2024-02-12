import os
import pytest
from oi_chatbot.utils import preprocess_profile


def test_preprocess_profile():
    if os.getenv('GITHUB_ACTIONS') == 'true':
        return

    profile = {
        'aws_profile': 'default'
    }
    preprocess_profile(profile)
    assert 'AWS_ACCESS_KEY_ID' in os.environ
    assert 'AWS_SECRET_ACCESS_KEY' in os.environ
    assert 'AWS_REGION_NAME' in os.environ


if __name__ == '__main__':
    pytest.main()
