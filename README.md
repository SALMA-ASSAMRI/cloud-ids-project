# Cloud IDS — Détection d'intrusion avec IA sur LocalStack

## Description
Système de détection d'intrusion cloud utilisant un modèle ML (Random Forest)
pour analyser les accès S3 en temps réel et alerter via SNS.

## Technologies
- LocalStack (simulation AWS locale)
- AWS Lambda, S3, SNS, DynamoDB
- Python, scikit-learn, boto3

## Lancer le projet
1. `docker-compose up` pour démarrer LocalStack
2. `bash setup/setup_localstack.sh` pour configurer les services
3. `python model/generate_dataset.py` pour générer les données
4. `python model/train_model.py` pour entraîner le modèle
5. `python tests/simulate_attack.py` pour tester