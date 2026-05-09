@echo off
echo === Installation Cloud IDS Project ===

echo 1. Installation des dependances Python...
pip install boto3 scikit-learn pandas numpy joblib awscli-local

echo 2. Generation du dataset...
python model/generate_dataset.py

echo 3. Entrainement du modele ML...
python model/train_model.py

echo 4. Copie du modele...
copy model\ids_model.pkl lambda\ids_model.pkl

echo 5. Creation du ZIP Lambda...
python create_zip.py

echo 6. Configuration LocalStack...
awslocal s3 mb s3://bucket-protege
awslocal dynamodb create-table --table-name AccessLogs --attribute-definitions AttributeName=log_id,AttributeType=S --key-schema AttributeName=log_id,KeyType=HASH --billing-mode PAY_PER_REQUEST
awslocal sns create-topic --name IntrusionAlerts
awslocal sqs create-queue --queue-name AlertesQueue
awslocal sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:IntrusionAlerts --protocol sqs --notification-endpoint arn:aws:sqs:us-east-1:000000000000:AlertesQueue
awslocal lambda create-function --function-name IDS-Lambda --runtime python3.11 --role arn:aws:iam::000000000000:role/lambda-role --handler lambda_function.lambda_handler --zip-file fileb://lambda/function.zip --timeout 30

echo 7. Lancement du dashboard...
python server.py

pause