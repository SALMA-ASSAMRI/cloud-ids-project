import boto3, json

lambda_client = boto3.client("lambda",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test")

acces_suspect = {
    "timestamp":              "2025-05-09T02:34:00",
    "ip_source":              "185.220.101.45",
    "bucket":                 "bucket-protege",
    "methode_http":           "DELETE",
    "nb_requetes_par_minute": 847,
    "nb_fichiers_accedes":    312,
    "taille_totale_mb":       2840,
    "pays":                   "RU"
}

print("Envoi d'un accès suspect...")
response = lambda_client.invoke(
    FunctionName="IDS-Lambda",
    Payload=json.dumps(acces_suspect)
)
result = json.loads(response["Payload"].read())
print(f"Résultat : {result}")

# Vérifier l'alerte dans SQS
sqs = boto3.client("sqs",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test")

messages = sqs.receive_message(
    QueueUrl="http://localhost:4566/000000000000/AlertesQueue",
    MaxNumberOfMessages=5
)
print(f"\nAlertes reçues dans SQS : {len(messages.get('Messages', []))}")
for msg in messages.get("Messages", []):
    print(json.dumps(json.loads(msg["Body"]), indent=2))