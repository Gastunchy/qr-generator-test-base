from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
secret_name = "projects/970772571927/secrets/test-base-secret/versions/latest"
secret = client.access_secret_version(request={"name": secret_name}).payload.data.decode("UTF-8")

print (secret)