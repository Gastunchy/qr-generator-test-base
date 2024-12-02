from google.cloud import secretmanager
client = secretmanager.SecretManagerServiceClient()
secret_version_name = "projects/970772571927/secrets/qr-generator-secrets/versions/latest"
response = client.access_secret_version(request={"name": secret_version_name})
env = response.payload.data.decode("UTF-8")
print(f"{env}")
