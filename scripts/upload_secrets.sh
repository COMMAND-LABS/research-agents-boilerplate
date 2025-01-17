#!/bin/bash

# Set your Google Cloud project ID
PROJECT_ID="kalygo-436411"
SECRET_PREFIX="RESEARCH_AGENTS"

# Path to your .env file
ENV_FILE=".env"

# Check if the .env file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: .env file not found!"
  exit 1
fi

# Loop through each line in the .env file
while IFS='=' read -r key value || [ -n "$key" ]; do
  # Skip empty lines and comments
  if [[ -z "$key" || "$key" == \#* ]]; then
    continue
  fi

  # Trim whitespace from key and value
  key=$(echo "$key" | xargs)
  value=$(echo "$value" | xargs)

  # Create the secret in Google Secret Manager
  echo "Secret: $key"
  FULL_SECRET_NAME="${SECRET_PREFIX}_${key}"
  echo "Creating $SECRET_NAME in Google Secret Manager"
  echo ""
  echo -n "$value" | gcloud secrets create "$FULL_SECRET_NAME" \
    --replication-policy="automatic" \
    --data-file=-
done < "$ENV_FILE"

echo "All secrets have been created in Google Secret Manager."