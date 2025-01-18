#!/bin/bash


# Set your Google Cloud project ID
PROJECT_NUMBER="830723611668"
SECRET_PREFIX="RESEARCH_AGENTS"

# Path to your .env file
ENV_FILE=".env"

# Check if the .env file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: .env file not found!"
  exit 1
fi

# Loop through each line in the .env file
secrets_string=""
while IFS='=' read -r key value || [ -n "$key" ]; do
  # Skip empty lines and comments
  if [[ -z "$key" || "$key" == \#* ]]; then
    continue
  fi

  # Trim whitespace from key and value
  key=$(echo "$key" | xargs)
  value=$(echo "$value" | xargs)

  # Build the secrets string
  secrets_string+="${key}=projects/${PROJECT_NUMBER}/secrets/${SECRET_PREFIX}_${key}:latest,"
done < "$ENV_FILE"

# Remove the trailing comma
secrets_string=${secrets_string%,}

# Output the secrets string
echo $secrets_string