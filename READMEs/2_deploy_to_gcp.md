# TLDR

Documenting steps of deploying to GCP (aka the cloud)

## Test the application in Docker

Add a Dockerfile

- `touch Dockerfile` <!-- populate -->
- `docker rmi $(docker images -q)` <!-- delete all images -->
- `docker images`
- `docker build -t research-agents .`
- `docker images`
- `docker run research-agents` <!-- this is some amateur shit tho -->
- `touch .dockerignore`
- `touch docker-compose.yml` <!-- populate -->
- `docker-compose up`

## Deploy to GCP

Jobs (One-off scripts) vs. Services (Long-running processes)

```sh
PROJECT_ID=kalygo-436411
gcloud --version
gcloud auth login

# https://console.cloud.google.com/artifacts/browse/kalygo-436411?project=kalygo-436411
gcloud artifacts repositories create research-agents-repo \
    --repository-format=docker \
    --location=us-east1 \
    --description="Repo for holding images related to the Research Agents"
gcloud auth configure-docker us-east1-docker.pkg.dev
docker build --platform linux/amd64 -f Dockerfile -t us-east1-docker.pkg.dev/$PROJECT_ID/research-agents-repo/research-agents:latest . ## the "platform" flag is key
docker push us-east1-docker.pkg.dev/$PROJECT_ID/research-agents-repo/research-agents:latest
```

CHECK OUT THE FOLLOWING URL BEFORE AND AFTER PUSHING: `https://console.cloud.google.com/artifacts/docker/kalygo-436411/us-east1/research-agents-repo`

## Now that the image is stored in GCP we can run it just like we ran it locally

First deploy the image to GCR...

```sh
JOB_NAME=research-agents
IMAGE_URL=us-east1-docker.pkg.dev/kalygo-436411/research-agents-repo/research-agents:latest
CLOUD_RUN_REGION=us-east1
PROJECT_ID=kalygo-436411

gcloud run jobs deploy $JOB_NAME \
  --image=$IMAGE_URL \
  --region=$CLOUD_RUN_REGION \
  --max-retries=3 \
  --memory=1Gi \
  --project $PROJECT_ID  
```

Second run the image with GCR...

```sh
gcloud run jobs execute research-agents \
  --region=us-east1
```

## OOPS! - we need to give our container the environment variables

- `touch scripts/upload_secrets.sh`
- `chmod +x scripts/upload_secrets.sh`
- `./scripts/upload_secrets.sh`

CHECK OUT: `https://console.cloud.google.com/security/secret-manager?project=kalygo-436411`

## Redeploy the Cloud Run Job

```sh
PROJECT_NUMBER=830723611668
PROJECT_ID=kalygo-436411
# peep the scripts/build_set_secrets_string.sh script
gcloud run jobs deploy research-agents \
    --image $IMAGE_URL \
    --set-secrets "OPENAI_API_KEY=projects/$PROJECT_NUMBER/secrets/RESEARCH_AGENTS_OPENAI_API_KEY:latest,AWS_SECRET_KEY=projects/$PROJECT_NUMBER/secrets/RESEARCH_AGENTS_AWS_SECRET_KEY:latest,AWS_ACCESS_KEY_ID=projects/$PROJECT_NUMBER/secrets/RESEARCH_AGENTS_AWS_ACCESS_KEY_ID:latest,AWS_REGION=projects/$PROJECT_NUMBER/secrets/RESEARCH_AGENTS_AWS_REGION:latest,AGENTOPS_API_KEY=projects/830723611668/secrets/RESEARCH_AGENTS_AGENTOPS_API_KEY:latest,MAILING_LIST=projects/830723611668/secrets/RESEARCH_AGENTS_MAILING_LIST:latest" \
    --memory 1Gi \
    --max-retries 5 \
    --region us-east1 \
    --project $PROJECT_ID

gcloud run jobs execute research-agents \
  --region=us-east1
```

In case you run into permissions errors

```sh
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

And run the image with GCR again ...

```sh
gcloud run jobs execute research-agents \
  --region=us-east1
```

CHECK OUT: `https://console.cloud.google.com/run/jobs/details/us-east1/research-agents-crew/logs?project=kalygo-436411`

## Now for the sauce...

Google Cloud Run Scheduler

```sh
SCHEDULER_JOB_NAME=research_agents_scheduler
SCHEDULER_REGION=us-east1
CLOUD_RUN_REGION=us-east1
PROJECT_ID=kalygo-436411
PROJECT_NUMBER=830723611668
JOB_NAME=research-agents
CRON_EXPRESSION="0 0 * * 1,4"
gcloud scheduler jobs create http $SCHEDULER_JOB_NAME \
  --location $SCHEDULER_REGION \
  --schedule="$CRON_EXPRESSION" \
  --uri="https://$CLOUD_RUN_REGION-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$PROJECT_ID/jobs/${JOB_NAME}:run" \
  --http-method POST \
  --oauth-service-account-email $PROJECT_NUMBER-compute@developer.gserviceaccount.com
```
