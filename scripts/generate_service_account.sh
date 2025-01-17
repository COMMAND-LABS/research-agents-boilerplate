#!/bin/bash

SERVICE_ACCOUNT_NAME="research-agents-cicd"
SERVICE_ACCOUNT_KEY_FILE="research-agents-cicd-sa.json"
ARTIFACTORY_REPO_NAME=research-agents-repo
PROJECT_NUMBER=830723611668

gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
  --description="Service account for GitHub Actions CI/CD for the Research Agents" \
  --display-name="Research Agents CICD"

gcloud artifacts repositories add-iam-policy-binding $ARTIFACTORY_REPO_NAME \
  --location=us-east1 \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME@kalygo-436411.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding kalygo-436411 \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME@kalygo-436411.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"

gcloud projects add-iam-policy-binding kalygo-436411 \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME@kalygo-436411.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding kalygo-436411 \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME@kalygo-436411.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud iam service-accounts add-iam-policy-binding $PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME@kalygo-436411.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

gcloud iam service-accounts keys create $SERVICE_ACCOUNT_KEY_FILE \
  --iam-account="$SERVICE_ACCOUNT_NAME@kalygo-436411.iam.gserviceaccount.com"