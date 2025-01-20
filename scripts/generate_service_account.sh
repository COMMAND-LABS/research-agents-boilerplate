#!/bin/bash

PROJECT_ID="kalygo-436411"
PROJECT_NUMBER="830723611668"
SERVICE_ACCOUNT_NAME="research-agents-cicd"
SERVICE_ACCOUNT_EMAIL="research-agents-cicd@$PROJECT_ID.iam.gserviceaccount.com"
SERVICE_ACCOUNT_DESCRIPTION="Service account description"
SERVICE_ACCOUNT_DISPLAY_NAME="Service account display name"
SERVICE_ACCOUNT_KEY_FILE="research-agents-cicd-sa.json"
ARTIFACTORY_REPO_NAME="research-agents-repo"

gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
  --description="$SERVICE_ACCOUNT_DESCRIPTION" \
  --display-name="$SERVICE_ACCOUNT_DISPLAY_NAME"

gcloud artifacts repositories add-iam-policy-binding $ARTIFACTORY_REPO_NAME \
  --location=us-east1 \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/artifactregistry.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/run.admin"

gcloud iam service-accounts add-iam-policy-binding $PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/iam.serviceAccountUser"

gcloud iam service-accounts keys create $SERVICE_ACCOUNT_KEY_FILE \
  --iam-account="$SERVICE_ACCOUNT_EMAIL"