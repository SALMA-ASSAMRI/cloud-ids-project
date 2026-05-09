import boto3, json, uuid, joblib
import numpy as np
from datetime import datetime

ENDPOINT  = "http://localhost:4566"
REGION    = "us-east-1"
TOPIC_ARN = "arn:aws:sns:us-east-1:000000000000:IntrusionAlerts"
SEUIL     = 0.7

modele = joblib.load("/var/task/ids_model.pkl")

def get_client(service):
    return boto3.client(service,
        endpoint_url=ENDPOINT, region_name=REGION,
        aws_access_key_id="test", aws_secret_access_key="test")

def extraire_features(log):
    heure     = datetime.fromisoformat(
                    log.get("timestamp","2025-01-01T12:00:00")).hour
    ip        = log.get("ip_source","0.0.0.0")
    whitelist = ["192.168.1.1","10.0.0.1","172.16.0.1"]
    return np.array([[
        heure,
        log.get("nb_requetes_par_minute", 1),
        log.get("nb_fichiers_accedes", 1),
        log.get("taille_totale_mb", 0.1),
        1 if ip in whitelist else 0,
        1 if log.get("pays","MA") not in ["MA","FR","US"] else 0,
        1 if log.get("methode_http","GET") == "DELETE" else 0,
    ]])

def publier_alerte(log, score):
    sns = get_client("sns")
    message = {
        "type":      "INTRUSION_DETECTEE",
        "score":     round(score, 3),
        "ip":        log.get("ip_source"),
        "timestamp": log.get("timestamp"),
        "bucket":    log.get("bucket"),
        "fichiers":  log.get("nb_fichiers_accedes"),
        "methode":   log.get("methode_http"),
    }
    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject=f"ALERTE IDS — Score: {score:.2f} — IP: {log.get('ip_source')}",
        Message=json.dumps(message, indent=2),
        MessageAttributes={
            "type_alerte": {"DataType":"String","StringValue":"INTRUSION"},
            "score":       {"DataType":"Number","StringValue":str(round(score,3))},
        }
    )

def logger_dynamo(log, score, est_suspect):
    dynamodb = get_client("dynamodb")
    dynamodb.put_item(
        TableName="AccessLogs",
        Item={
            "log_id":      {"S": str(uuid.uuid4())},
            "timestamp":   {"S": log.get("timestamp", datetime.utcnow().isoformat())},
            "ip_source":   {"S": log.get("ip_source","inconnu")},
            "bucket":      {"S": log.get("bucket","inconnu")},
            "methode":     {"S": log.get("methode_http","GET")},
            "nb_fichiers": {"N": str(log.get("nb_fichiers_accedes",1))},
            "score_ml":    {"N": str(round(score,4))},
            "statut":      {"S": "SUSPECT" if est_suspect else "NORMAL"},
        }
    )

def lambda_handler(event, context):
    print(f"Log reçu : {json.dumps(event)}")
    features    = extraire_features(event)
    probas      = modele.predict_proba(features)[0]
    score       = float(probas[1])
    est_suspect = score >= SEUIL

    print(f"Score : {score:.3f} → {'SUSPECT' if est_suspect else 'NORMAL'}")

    if est_suspect:
        publier_alerte(event, score)
        print(f"Alerte SNS envoyée !")

    logger_dynamo(event, score, est_suspect)

    return {
        "statusCode": 200,
        "score":      round(score, 3),
        "statut":     "SUSPECT" if est_suspect else "NORMAL"
    }