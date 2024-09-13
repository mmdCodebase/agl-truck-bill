import boto3

def get_aws_secret(secret_name):
    # Create a Secrets Manager client
    client = boto3.client(
        service_name='secretsmanager',
        region_name='us-east-1',)
    # Retrieve the secret value
    response = client.get_secret_value(SecretId=secret_name)
    secret_value = response["SecretString"]
    
    return secret_value