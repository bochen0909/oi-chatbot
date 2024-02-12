
import os


def get_aws_credentials(profile_name):
    import boto3
    session = boto3.Session(profile_name=profile_name)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    return aws_access_key_id, aws_secret_access_key, os.getenv('AWS_REGION', 'us-east-1')


def preprocess_profile(profile: dict):
    if 'aws_profile' in profile:
        aws_access_key_id, aws_secret_access_key, aws_region = get_aws_credentials(
            profile['aws_profile'])
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        os.environ['AWS_REGION_NAME'] = aws_region
    elif profile['llm']['model'].startswith('gpt'):
        assert "OPENAI_API_KEY" in os.environ, "OpenAI API key not found in environment"
    return profile


def apply_profile(self, selected_profile):
    preprocess_profile(selected_profile)
    for key, value in selected_profile.get('llm', {}).items():
        setattr(self.llm, key, value)
    if 'custom_instructions' in selected_profile:
        self.llm.custom_instructions = selected_profile['custom_instructions']
    return self
